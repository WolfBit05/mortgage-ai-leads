from app.scraper.reddit import scrape_reddit
from app.database.repository import DiscussionRepository
from app.database.db import SessionLocal

def run():
    print("Starting Reddit pipeline...")

    discussions = scrape_reddit()

    db = SessionLocal()
    repo = DiscussionRepository(db)

    for discussion in discussions:

        if repo.exists(discussion.url):
            print(f"⏭ Skipped: {discussion.title}")
            continue

        repo.save(discussion)
        print(f"✅ Saved: {discussion.title}")
        
    repo.commit()
    db.close()

    print("Pipeline completed.")