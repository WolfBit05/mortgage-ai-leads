import json

from app.database.models import Discussion
from app.models.discussion_data import DiscussionData
from app.ai.intent_detector import IntentResult

class DiscussionRepository:

    def __init__(self, db):
        self.db = db

    def get_by_url(self, url):
        return (
        self.db.query(Discussion)
        .filter(Discussion.url == url)
        .first()
    )

    def update(self, discussion, discussion_data: DiscussionData):
        discussion.content = discussion_data.content
        discussion.score = discussion_data.score
        discussion.comments_count = discussion_data.comments_count

    def update_intent(
        self,
        discussion,
        intent_result: IntentResult
    ):
        discussion.primary_intent = intent_result.primary_intent.type
        discussion.primary_confidence = intent_result.primary_intent.confidence

        if intent_result.secondary_intent:
            discussion.secondary_intent = (
                intent_result.secondary_intent.type
            )
            discussion.secondary_confidence = (
                intent_result.secondary_intent.confidence
            )
        else:
            discussion.secondary_intent = None
            discussion.secondary_confidence = None

        discussion.signals = json.dumps(intent_result.signals)
        discussion.intent_summary = intent_result.summary

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

        return discussion

    def commit(self):
        self.db.commit()