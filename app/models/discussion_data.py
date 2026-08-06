from dataclasses import dataclass
from datetime import datetime

@dataclass
class DiscussionData:
    platform: str
    url: str
    author: str
    title: str
    content: str
    subreddit: str | None
    flair: str | None
    score: int | None
    comments_count: int | None
    created_at: datetime