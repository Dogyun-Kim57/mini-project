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
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.common.exceptions import ValidationException, AuthException


class AuthService:
    LOGIN_FAIL_LIMIT = 5
    LOCK_MINUTES = 1

    @staticmethod
    def signup(data):
        # 이메일 중복 검사
        if UserRepository.get_by_email(data["email"]):
            raise ValidationException("이미 사용 중인 이메일입니다.", 409)

        # 비밀번호 암호화
        password_hash = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

        user = User(
            email=data["email"],
            password_hash=password_hash,
            name=data["name"],
            role="user",
            is_active=True,
            login_fail_count=0,
            lock_until=None,
            deleted_at=None
        )

        saved_user = UserRepository.create_user(user)
        return saved_user.to_dict()

    @staticmethod
    def login(data):
        email = data["email"]
        input_password = data["password"]

        user = UserRepository.get_by_email(email)

        # 회원 없음 또는 탈퇴 처리됨
        if not user or user.deleted_at is not None:
            raise AuthException("이메일 또는 비밀번호가 올바르지 않습니다.", 401)

        # 비활성 계정
        if not user.is_active:
            raise AuthException("비활성화된 계정입니다.", 403)

        now = datetime.utcnow()

        # 잠금 상태 확인
        if user.lock_until and user.lock_until > now:
            remain_seconds = int((user.lock_until - now).total_seconds())
            raise AuthException(
                f"로그인 5회 이상 실패로 잠금 상태입니다. {remain_seconds}초 후 다시 시도해주세요.",
                403
            )

        # 비밀번호 틀림
        if not bcrypt.check_password_hash(user.password_hash, input_password):
            user.login_fail_count += 1

            if user.login_fail_count >= AuthService.LOGIN_FAIL_LIMIT:
                user.lock_until = now + timedelta(minutes=AuthService.LOCK_MINUTES)
                user.login_fail_count = 0

            UserRepository.save()
            raise AuthException("이메일 또는 비밀번호가 올바르지 않습니다.", 401)

        # 로그인 성공
        user.login_fail_count = 0
        user.lock_until = None
        UserRepository.save()

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "email": user.email,
                "role": user.role
            }
        )

        return {
            "access_token": access_token,
            "user": user.to_dict()
        }

    @staticmethod
    def get_me(user_id):
        user = UserRepository.get_by_id(user_id)

        if not user or user.deleted_at is not None:
            raise AuthException("사용자를 찾을 수 없습니다.", 404)

        return user.to_dict()