def validate_member_update(data):
    allowed_fields = ["email", "name", "status", "role", "admin_code"]

    for key in data.keys():
        if key not in allowed_fields:
            return False, f"허용되지 않은 필드입니다: {key}"

    return True, None