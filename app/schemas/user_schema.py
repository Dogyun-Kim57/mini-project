# 회원 수정 API용 입력값 검사 기능

def validate_user_update(data):
    allowed_fields = ["email", "name", "role", "is_active"]

    for key in data.keys():
        if key not in allowed_fields:
            return False, f"허용되지 않은 필드입니다: {key}"

    return True, None