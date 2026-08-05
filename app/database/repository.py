from app.database.models import Discussion


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

    def save(self, discussion):

        self.db.add(discussion)

    def commit(self):
        self.db.commit()