def validate_video_create(data):
    required_fields = ["member_id", "title", "original_filename", "saved_filename", "file_path"]

    for field in required_fields:
        if not data.get(field):
            return False, f"{field} 값은 필수입니다."

    return True, None


def validate_video_update(data):
    allowed_fields = ["title", "status", "duration_sec", "file_size"]

    for key in data.keys():
        if key not in allowed_fields:
            return False, f"허용되지 않은 필드입니다: {key}"

    return True, None