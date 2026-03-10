# 직접 정의한 예외 모음 파일
# 오류를 종류별로 구분해서 처리하는 용도

class AppException(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ValidationException(AppException):
    pass


class AuthException(AppException):
    pass


class NotFoundException(AppException):
    pass