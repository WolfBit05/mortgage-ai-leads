from app.scraper.reddit import scrape_reddit
from app.database.repository import DiscussionRepository
from app.database.db import SessionLocal

def run():
    print("Starting Reddit pipeline...")

    discussions = scrape_reddit()

    db = SessionLocal()
    repo = DiscussionRepository(db)

    for discussion in discussions:

        existing = repo.get_by_url(discussion.url)

        if existing:
            if not existing.content and discussion.content:
                repo.update(existing, discussion)
                print(f"🔄 Updated: {discussion.title}")
            else:
                print(f"⏭ Skipped: {discussion.title}")
        else:
            repo.save(discussion)
            print(f"✅ Saved: {discussion.title}")
        
    repo.commit()
    db.close()

    print("Pipeline completed.")