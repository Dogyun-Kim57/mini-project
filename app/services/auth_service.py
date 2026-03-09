# 회원가입/로그인의 실제 핵심 로직
# 중복 확인, 비밀번호 암호화(해시), 회원 생성, 로그인 검증, JWT 토근 발급 등

# 핵심 포인트
# < 회원가입 >
# 1. 아이디 중복 검사
# 2. 이메일 중복 검사
# 3. 비밀번호 암호화
# 4. 회원 객체 생성
# 5. DB 저장

# < 로그인 >
# 1. 아이디로 회원 찾기
# 2. 비밀번호 비교
# 3. 상태 확인
# 4. JWT 토큰 발급

# 기존처럼 이 로직을 route에 넣으면, 디버깅 지옥이 예상되기에...
# service를 따로 빼서 이 파일이 실제 처리 로직 본체라고 생각하면 됨.

from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
from app.extensions import bcrypt
from app.models.member_model import Member
from app.repositories.member_repository import MemberRepository
from app.common.exceptions import ValidationException, AuthException


class AuthService:
    LOGIN_FAIL_LIMIT = 5
    LOCK_MINUTES = 1

    @staticmethod
    def signup(data):
        # uid 중복 체크
        if MemberRepository.get_by_uid(data["uid"]):
            raise ValidationException("이미 사용 중인 uid입니다.", 409)

        # email 중복 체크
        if MemberRepository.get_by_email(data["email"]):
            raise ValidationException("이미 사용 중인 이메일입니다.", 409)

        # 비밀번호 해시 처리
        password_hash = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

        # 관리자 코드가 맞으면 관리자 계정 생성
        # 실제 운영에서는 하드코딩보다 .env 관리가 더 좋다
        role = "user"
        admin_code = data.get("admin_code")

        if admin_code and admin_code == "MASTER_ADMIN_CODE":
            role = "admin"

        member = Member(
            uid=data["uid"],
            email=data["email"],
            password=password_hash,
            name=data["name"],
            role=role,
            status="active",
            admin_code=admin_code
        )

        saved_member = MemberRepository.create_member(member)
        return saved_member.to_dict()

    @staticmethod
    def login(data):
        login_id = data["login_id"]
        input_password = data["password"]

        # uid 또는 email로 회원 찾기
        member = MemberRepository.get_by_login_id(login_id)

        if not member:
            raise AuthException("아이디(또는 이메일) 또는 비밀번호가 올바르지 않습니다.", 401)

        # 계정 상태 확인
        if member.status != "active":
            raise AuthException("비활성화된 계정입니다.", 403)

        # 로그인 제한 중인지 확인
        now = datetime.utcnow()
        if member.locked_until and member.locked_until > now:
            remain_seconds = int((member.locked_until - now).total_seconds())
            raise AuthException(
                f"로그인 5회 이상 실패로 제한되었습니다. {remain_seconds}초 후 다시 시도해주세요.",
                403
            )

        # 비밀번호 확인
        if not bcrypt.check_password_hash(member.password, input_password):
            member.login_fail_count += 1

            # 실패 횟수 5회 이상이면 1분 제한
            if member.login_fail_count >= AuthService.LOGIN_FAIL_LIMIT:
                member.locked_until = now + timedelta(minutes=AuthService.LOCK_MINUTES)
                member.login_fail_count = 0

            MemberRepository.save()
            raise AuthException("아이디(또는 이메일) 또는 비밀번호가 올바르지 않습니다.", 401)

        # 로그인 성공 시 실패 횟수 초기화
        member.login_fail_count = 0
        member.locked_until = None
        member.last_login = now
        MemberRepository.save()

        # JWT 발급
        access_token = create_access_token(
            identity=str(member.id),
            additional_claims={
                "uid": member.uid,
                "role": member.role
            }
        )

        return {
            "access_token": access_token,
            "member": member.to_dict()
        }

    @staticmethod
    def get_me(member_id):
        member = MemberRepository.get_by_id(member_id)
        if not member:
            raise AuthException("사용자를 찾을 수 없습니다.", 404)

        return member.to_dict()