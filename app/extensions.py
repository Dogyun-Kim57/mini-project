# Flask 확장 기능을 따로 모아두는 파일
# DB, 암호화, JWT 같은 확장 기능 객체들을 미리 생성
# 마치 공용 장비 보관실 같은 개념

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()