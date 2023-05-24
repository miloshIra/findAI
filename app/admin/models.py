from sqlalchemy import func
from ..app import app, db


class Dashboard():
    @classmethod
    def group_and_count_users(cls):
        """
        Counts all users

        :return: dict
        """
        return Dashboard._group_and_count(User, User.role)
    
    @classmethod
    def _group_and_count(cls, model, field):
        count = func.count(field)
        query = db.session.query(count, field).group_by(field).all()

        results = {
            'query': query,
            'total': model.query.count()
        }

        return results