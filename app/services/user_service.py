
# 회원관리 전용 로직

from datetime import datetime
from app.repositories.user_repository import UserRepository
from app.common.exceptions import NotFoundException


class UserService:
    @staticmethod
    def get_user_list():
        users = UserRepository.get_all_active_users()
        return [user.to_dict() for user in users]

    @staticmethod
    def get_user_detail(user_id):
        user = UserRepository.get_by_id(user_id)

        if not user or user.deleted_at is not None:
            raise NotFoundException("회원을 찾을 수 없습니다.", 404)

        return user.to_dict()

    @staticmethod
    def update_user(user_id, data):
        user = UserRepository.get_by_id(user_id)

        if not user or user.deleted_at is not None:
            raise NotFoundException("회원을 찾을 수 없습니다.", 404)

        if "email" in data:
            user.email = data["email"]
        if "name" in data:
            user.name = data["name"]
        if "role" in data:
            user.role = data["role"]
        if "is_active" in data:
            user.is_active = data["is_active"]

        UserRepository.save()
        return user.to_dict()

    @staticmethod
    def deactivate_user(user_id):
        user = UserRepository.get_by_id(user_id)

        if not user or user.deleted_at is not None:
            raise NotFoundException("회원을 찾을 수 없습니다.", 404)

        user.is_active = False
        UserRepository.save()
        return user.to_dict()

    @staticmethod
    def soft_delete_user(user_id):
        user = UserRepository.get_by_id(user_id)

        if not user or user.deleted_at is not None:
            raise NotFoundException("회원을 찾을 수 없습니다.", 404)

        user.deleted_at = datetime.utcnow()
        user.is_active = False
        UserRepository.save()

        return {"deleted_user_id": user_id}