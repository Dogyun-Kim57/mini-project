from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.common.decorators import admin_required
from app.common.response import success_response, error_response
from app.common.exceptions import AppException
from app.schemas.user_schema import validate_user_update
from app.services.user_service import UserService

user_bp = Blueprint("user", __name__)


@user_bp.route("", methods=["GET"])
@jwt_required()
@admin_required
def get_user_list():
    try:
        result = UserService.get_user_list()
        return success_response("회원 목록 조회 성공", result)
    except AppException as e:
        return error_response(e.message, status_code=e.status_code)


@user_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_detail(user_id):
    try:
        result = UserService.get_user_detail(user_id)
        return success_response("회원 상세 조회 성공", result)
    except AppException as e:
        return error_response(e.message, status_code=e.status_code)


@user_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_user(user_id):
    data = request.get_json() or {}

    is_valid, error = validate_user_update(data)
    if not is_valid:
        return error_response(error, status_code=400)

    try:
        result = UserService.update_user(user_id, data)
        return success_response("회원 정보 수정 성공", result)
    except AppException as e:
        return error_response(e.message, status_code=e.status_code)


@user_bp.route("/<int:user_id>/deactivate", methods=["PATCH"])
@jwt_required()
@admin_required
def deactivate_user(user_id):
    try:
        result = UserService.deactivate_user(user_id)
        return success_response("회원 비활성화 성공", result)
    except AppException as e:
        return error_response(e.message, status_code=e.status_code)


@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def soft_delete_user(user_id):
    try:
        result = UserService.soft_delete_user(user_id)
        return success_response("회원 탈퇴(소프트 삭제) 성공", result)
    except AppException as e:
        return error_response(e.message, status_code=e.status_code)