# 모든 테이블에서 공통으로 사용할 기본 컬럼을 여기서 정의
# created_at 그리고 updated_at 같은 공통 컬럼을 중복 없이 관리

# 회원 테이블에도 생성일이 필요하고
# 영상 테이블에도 생성일이 필요하고
# 분석 결과에도 생성일이 필요할 수 있다.
# 그걸 매번 적지 말고 부모 클래스로 빼는 용도

from datetime import datetime
from app.extensions import db


class BaseModel(db.Model):
    """
    모든 테이블에서 공통으로 사용할 생성일 / 수정일 컬럼
    """
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

