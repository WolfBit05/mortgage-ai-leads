from app.database.models import Discussion
from app.models.discussion_data import DiscussionData


class DiscussionRepository:

    def __init__(self, db):
        self.db = db

    def exists(self, url):
        return (
        self.db.query(Discussion)
        .filter(Discussion.url == url)
        .first()
        is not None
    )


    def save(self, discussion_data: DiscussionData):

        discussion = Discussion(
            platform=discussion_data.platform,
            url=discussion_data.url,
            title=discussion_data.title,
            author=discussion_data.author,
            content=discussion_data.content,
            subreddit=discussion_data.subreddit,
            flair=discussion_data.flair,
            score=discussion_data.score,
            comments_count=discussion_data.comments_count,
            created_at=discussion_data.created_at,

        )

        self.db.add(discussion)

    def commit(self):
        self.db.commit()