from app.extensions import db
from app.models.base_model import BaseModel


class User(BaseModel):
    """
    users 테이블 모델
    회원가입, 로그인, 회원관리, 관리자 권한 구분에 사용
    """
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True)

    # 로그인 이메일
    email = db.Column(db.String(100), unique=True, nullable=False)

    # 암호화된 비밀번호
    password_hash = db.Column(db.String(255), nullable=False)

    # 회원 이름
    name = db.Column(db.String(50), nullable=False)

    # 권한 구분
    role = db.Column(
        db.Enum("user", "admin", name="user_role_enum"),
        nullable=False,
        default="user"
    )

    # 활성 회원 여부
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # 로그인 실패 횟수
    login_fail_count = db.Column(db.Integer, nullable=False, default=0)

    # 로그인 잠금 해제 시간
    lock_until = db.Column(db.DateTime, nullable=True)

    # 탈퇴 처리 시각 (소프트 삭제)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        """
        응답용 딕셔너리 변환
        비밀번호는 절대 반환하지 않음
        """
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role,
            "is_active": self.is_active,
            "login_fail_count": self.login_fail_count,
            "lock_until": self.lock_until.isoformat() if self.lock_until else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }