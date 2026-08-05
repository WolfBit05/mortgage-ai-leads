from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.database.db import Base


class Discussion(Base):
    __tablename__ = "discussions"

    id = Column(Integer, primary_key=True, index=True)

    platform = Column(String(50), index=True)

    url = Column(String(500), unique=True, index=True)

    author = Column(String(200))

    title = Column(String(500))

    content = Column(Text)

    created_at = Column(DateTime)

    scraped_at = Column(DateTime, default=datetime.utcnow)