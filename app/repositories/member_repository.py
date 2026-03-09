# DB와 직접 통신하는 파일

# 회원 저장, 회원 조회, 회원 수정, 회원 삭제 같은 DB 관련 작업만 담당한다.

# 지금까지는 초보자는 종종 라우트 안에서 바로 DB 쿼리를 썼는데,
# 이러면 구조가 금방 복잡해진다.
# 협업이라는 특성상 최대한 디버깅의 난이도를 줄이기 위해 DB관련 코드는 이곳에 넣었음.

# 즉, route는 요청 받기 service는 판단하기
# 그리고 repository는 DB 다루기

from sqlalchemy import or_
from app.extensions import db
from app.models.member_model import Member


class MemberRepository:
    @staticmethod
    def create_member(member):
        db.session.add(member)
        db.session.commit()
        return member

    @staticmethod
    def get_by_uid(uid):
        return Member.query.filter_by(uid=uid).first()

    @staticmethod
    def get_by_email(email):
        return Member.query.filter_by(email=email).first()

    @staticmethod
    def get_by_id(member_id):
        return db.session.get(Member, member_id)

    @staticmethod
    def get_by_login_id(login_id):
        """
        uid 또는 email 둘 다 로그인 가능하게 조회
        """
        return Member.query.filter(
            or_(Member.uid == login_id, Member.email == login_id)
        ).first()

    @staticmethod
    def get_all():
        return Member.query.order_by(Member.id.desc()).all()

    @staticmethod
    def save():
        db.session.commit()

    @staticmethod
    def delete(member):
        db.session.delete(member)
        db.session.commit()