# 사용자의 요청을 직접 받는 파일

# < 역할 >
# URL 연결
# request 받기
# schema 호출
# service 호출
# 응답 반환

# route는 입구 개념
# 누가 요청했는지 받고, 데이터를 꺼내고
#검사하고, 처리 맡기고, 결과를 돌려준다.
# 즉, 직접 일하는 곳이 아니라 연결해주는 곳의 개념!

# 요청을 보냈을 시 흐름!

# 1. run.py가 서버를 실행 중
# 2. app/__init__.py에 등록된 auth_bp가 요청을 받음
# 3. auth_routes.py 의 signup() 실행
# 4. request.get_json()으로 입력값 받음
# 5. auth_schema.py 로 필수값 검사
# 6. auth_service.py 로 회원가입 로직 수행
# 7. member_repository.py 로 DB 저장
# 8. member_model.py 형태대로 members 테이블에 저장
# 9. response.py 로 성공 응답 반환

from flask import Blueprint, request
from app.common.response import success_response, error_response
from app.common.exceptions import AppException
from app.schemas.auth_schema import validate_signup, validate_login
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}

    is_valid, error = validate_signup(data)
    if not is_valid:
        return error_response(error, status_code=400)

    try:
        result = AuthService.signup(data)
        return success_response("회원가입이 완료되었습니다.", result, 201)
    except AppException as e:
        return error_response(e.message, status_code=e.status_code)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    is_valid, error = validate_login(data)
    if not is_valid:
        return error_response(error, status_code=400)

    try:
        result = AuthService.login(data)
        return success_response("로그인에 성공했습니다.", result, 200)
    except AppException as e:
        return error_response(e.message, status_code=e.status_code)