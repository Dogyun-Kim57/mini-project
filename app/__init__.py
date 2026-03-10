# 이 파일은 Flask 앱을 실제로 조립하는 공장 같은 역할

from flask import Flask
from app.config import Config
from app.extensions import db, bcrypt, jwt, migrate
from app.api.auth_routes import auth_bp
from app.api.user_routes import user_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")

    return app