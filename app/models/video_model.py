from app.extensions import db
from app.models.base_model import BaseModel


class Video(BaseModel):
    """
    영상 업로드 정보 테이블
    실제 영상 파일 자체를 DB에 넣는 것이 아니라,
    파일명 / 경로 / 업로드 상태 / 업로더 정보를 저장한다.
    """

    __tablename__ = "videos"

    # 영상 고유 번호
    id = db.Column(db.Integer, primary_key=True)

    # 업로드한 회원 번호
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)

    # 영상 제목
    title = db.Column(db.String(200), nullable=False)

    # 원본 파일명
    original_filename = db.Column(db.String(255), nullable=False)

    # 서버 저장 파일명
    saved_filename = db.Column(db.String(255), nullable=False)

    # 서버 저장 경로
    file_path = db.Column(db.String(500), nullable=False)

    # 파일 크기(byte)
    file_size = db.Column(db.BigInteger, nullable=True)

    # 영상 길이(초)
    duration_sec = db.Column(db.Integer, nullable=True)

    # 분석 상태
    # uploaded / processing / completed / failed
    status = db.Column(db.String(20), nullable=False, default="uploaded")

    def to_dict(self):
        return {
            "id": self.id,
            "member_id": self.member_id,
            "title": self.title,
            "original_filename": self.original_filename,
            "saved_filename": self.saved_filename,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "duration_sec": self.duration_sec,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }