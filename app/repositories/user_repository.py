from app.extensions import db
from app.models.user_model import User


class UserRepository:
    @staticmethod
    def create_user(user):
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_id(user_id):
        return db.session.get(User, user_id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_all_active_users():
        return User.query.filter_by(deleted_at=None).order_by(User.id.desc()).all()

    @staticmethod
    def save():
        db.session.commit()