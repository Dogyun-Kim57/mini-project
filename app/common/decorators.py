# 권한 검사 같은 공통 기능을 함수 형태로 만들어둔 파일!

# 관리자만 접근 가능한 API를 제한하는 용도

from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.common.response import error_response


# 함수가 실행되기 전에 먼저 JWT ( JSON Web Token )이 있는지 확인 하며,
# 토큰안의 Role(권한) 값을 확인한다.
# 즉, admin 권한이 아니면 차단하는 기능!

# 관리자 전용 기능을 매번 라우트마다 직접 쓰면 중복이 심해진다.
# 그래서 재사용 가능하게 빼는 거임.


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()

        if claims.get("role") != "admin":
            return error_response("관리자 권한이 필요합니다.", status_code=403)

        return fn(*args, **kwargs)

    return wrapper