from datetime import datetime

from app.models.discussion_data import DiscussionData
from app.browser.browser import launch_browser

MAX_POSTS = 5

SUBREDDIT_URL = "https://www.reddit.com/r/FirstTimeHomeBuyer/"


def scrape_reddit():

    playwright, context, page = launch_browser()

    print(f"Opening {SUBREDDIT_URL}")

    page.goto(
        SUBREDDIT_URL,
        wait_until="domcontentloaded"
    )

    page.wait_for_timeout(5000)

    posts = page.locator("shreddit-post")

    print(f"Found {posts.count()} posts\n")

    discussions = []

    try:
        for i in range(min(MAX_POSTS, posts.count())):
            post = posts.nth(i)

            title = post.get_attribute("post-title")
            author = post.get_attribute("author")
            permalink = post.get_attribute("permalink")
            created = post.get_attribute("created-timestamp")
            score = post.get_attribute("score")
            comments = post.get_attribute("comment-count")

            created_at = None
            if created:
                created_at = datetime.strptime(
                    created,
                    "%Y-%m-%dT%H:%M:%S.%f%z"
                )

                print("=" * 80)
                print(f"Title      : {title}")
                print(f"Author     : {author}")
                print(f"Created    : {created_at}")
                print(f"Score      : {score}")
                print(f"Comments   : {comments}")
                print(f"URL        : https://reddit.com{permalink}")

                if not title or not permalink:
                    continue

                url = "https://reddit.com" + permalink


                discussion = DiscussionData(
                platform="reddit",
                title=title,
                author=author,
                url=url,
                content="",
                subreddit="FirstTimeHomeBuyer",
                flair=None,
                score=int(score) if score else None,
                comments_count=int(comments) if comments else None,
                created_at=created_at
                )

                discussions.append(discussion)
        return discussions

    finally:
        context.close()
        playwright.stop()



if __name__ == "__main__":
    scrape_reddit()