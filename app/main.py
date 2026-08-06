from app.database.db import engine
from app.database.models import Base

from app.services.reddit_service import run

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    run()