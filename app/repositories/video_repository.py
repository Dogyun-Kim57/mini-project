from app.extensions import db
from app.models.video_model import Video


class VideoRepository:
    @staticmethod
    def create_video(video):
        db.session.add(video)
        db.session.commit()
        return video

    @staticmethod
    def get_all():
        return Video.query.order_by(Video.id.desc()).all()

    @staticmethod
    def get_by_id(video_id):
        return db.session.get(Video, video_id)

    @staticmethod
    def get_by_member_id(member_id):
        return Video.query.filter_by(member_id=member_id).order_by(Video.id.desc()).all()

    @staticmethod
    def save():
        db.session.commit()

    @staticmethod
    def delete(video):
        db.session.delete(video)
        db.session.commit()