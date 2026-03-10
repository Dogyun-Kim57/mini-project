# 회원가입/로그인 등 입력값 검증하는 파일
# 클라이언트가 보낸 JSON 데이터가 올바른지 여기서 확인

# 예를들어 로그인을 할때, UID만 넣고, 비밀번호를 기입 안했을 시..
# 서비스 로직으로 넘기면 에거라 나기 때문에, 먼저 검사하는 기능


def validate_signup(data):
    required_fields = ["email", "password", "name"]

    for field in required_fields:
        if not data.get(field):
            return False, f"{field} 값은 필수입니다."

    if len(data["password"]) < 4:
        return False, "비밀번호는 최소 4자 이상이어야 합니다."

    return True, None


def validate_login(data):
    required_fields = ["email", "password"]

    for field in required_fields:
        if not data.get(field):
            return False, f"{field} 값은 필수입니다."

    return True, None