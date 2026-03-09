# 해당 앱의 환경설정
# .env 파일의 값을 읽어서
# Flask에서 쓸 수 있는 설정값으로 변환

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask 보안 키
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # DB 접속 정보
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")
    DB_NAME = os.getenv("DB_NAME", "ai_mini_project")

    # SQLAlchemy에서 사용할 DB 접속 문자열
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT 설정
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))

    # 업로드 폴더
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 52428800))