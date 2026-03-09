from app.extensions import db
from app.models.base_model import BaseModel


class Member(BaseModel):
    """
    회원 테이블
    로그인, 권한관리, 계정상태, 로그인 제한 등을 관리
    """

    __tablename__ = "members"

    # 회원 고유 번호
    id = db.Column(db.Integer, primary_key=True)

    # 로그인용 아이디
    uid = db.Column(db.String(50), unique=True, nullable=False)

    # 이메일
    email = db.Column(db.String(100), unique=True, nullable=False)

    # 비밀번호 해시값
    password = db.Column(db.String(255), nullable=False)

    # 이름
    name = db.Column(db.String(50), nullable=False)

    # 권한
    # user / admin
    role = db.Column(db.String(20), nullable=False, default="user")

    # 상태
    # active / inactive / deleted
    status = db.Column(db.String(20), nullable=False, default="active")

    # 관리자 코드
    admin_code = db.Column(db.String(100), nullable=True)

    # 마지막 로그인 시간
    last_login = db.Column(db.DateTime, nullable=True)

    # 로그인 실패 횟수
    login_fail_count = db.Column(db.Integer, default=0, nullable=False)

    # 로그인 제한 해제 시각
    # 5회 이상 실패 시 현재 시간 + 1분 저장
    locked_until = db.Column(db.DateTime, nullable=True)

    # 회원이 업로드한 영상들과 연결
    videos = db.relationship("Video", backref="member", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "email": self.email,
            "name": self.name,
            "role": self.role,
            "status": self.status,
            "admin_code": self.admin_code,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "login_fail_count": self.login_fail_count,
            "locked_until": self.locked_until.isoformat() if self.locked_until else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }