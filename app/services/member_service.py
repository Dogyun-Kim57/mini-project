from app.repositories.member_repository import MemberRepository
from app.common.exceptions import NotFoundException


class MemberService:
    @staticmethod
    def get_member_list():
        members = MemberRepository.get_all()
        return [member.to_dict() for member in members]

    @staticmethod
    def get_member_detail(member_id):
        member = MemberRepository.get_by_id(member_id)

        if not member:
            raise NotFoundException("회원을 찾을 수 없습니다.", 404)

        return member.to_dict()

    @staticmethod
    def update_member(member_id, data):
        member = MemberRepository.get_by_id(member_id)

        if not member:
            raise NotFoundException("회원을 찾을 수 없습니다.", 404)

        if "email" in data:
            member.email = data["email"]
        if "name" in data:
            member.name = data["name"]
        if "status" in data:
            member.status = data["status"]
        if "role" in data:
            member.role = data["role"]
        if "admin_code" in data:
            member.admin_code = data["admin_code"]

        MemberRepository.save()
        return member.to_dict()

    @staticmethod
    def deactivate_member(member_id):
        member = MemberRepository.get_by_id(member_id)

        if not member:
            raise NotFoundException("회원을 찾을 수 없습니다.", 404)

        member.status = "inactive"
        MemberRepository.save()
        return member.to_dict()