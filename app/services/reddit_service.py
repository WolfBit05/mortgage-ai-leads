from app.scraper.reddit import scrape_reddit
from app.database.repository import DiscussionRepository
from app.database.db import SessionLocal
from app.ai.intent_detector import IntentDetector

def run():
    print("Starting Reddit pipeline...")

    discussions = scrape_reddit()

    db = SessionLocal()
    repo = DiscussionRepository(db)
    detector = IntentDetector()

    for discussion_data in discussions:

        existing = repo.get_by_url(discussion_data.url)

        if existing:

            content_updated = False

            if not existing.content and discussion_data.content:
                repo.update(existing, discussion_data)
                content_updated = True

                print(f"🔄 Updated: {discussion_data.title}")

            else:
                print(f"⏭ Skipped: {discussion_data.title}")

            discussion = existing

        else:
            discussion = repo.save(discussion_data)
            content_updated = True

            print(f"✅ Saved: {discussion_data.title}")

        # Run intent detection only when needed
        if discussion.content and (
            discussion.primary_intent is None
            or content_updated
        ):

            print(f"🤖 Detecting intent: {discussion.title}")

            intent_result = detector.detect(
                title=discussion.title,
                content=discussion.content,
            )

            repo.update_intent(
                discussion,
                intent_result
            )

            print(
                f"   → {intent_result.primary_intent.type} "
                f"({intent_result.primary_intent.confidence:.2f})"
            )

            if intent_result.secondary_intent:
                print(
                    f"   → secondary: "
                    f"{intent_result.secondary_intent.type} "
                    f"({intent_result.secondary_intent.confidence:.2f})"
                )

        else:
            print(f"🧠 Intent already exists: {discussion.title}")
        
    repo.commit()
    db.close()

    print("Pipeline completed.")