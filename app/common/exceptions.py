# 직접 정의한 예외 모음 파일
# 오류를 종류별로 구분해서 처리하는 용도

class AppException(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


# 아직은 pass 처리

# 입력 값 문제
class ValidationException(AppException):
    pass

# 로그인 문제
class AuthException(AppException):
    pass

# 데이터 없음
class NotFoundException(AppException):
    pass