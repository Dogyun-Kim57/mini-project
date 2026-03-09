from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.common.response import success_response, error_response
from app.common.exceptions import AppException
from app.schemas.video_schema import validate_video_create, validate_video_update
from app.services.video_service import VideoService

video_bp = Blueprint("video", __name__)


@video_bp.route("", methods=["POST"])
@jwt_required()
def create_video():
    data = request.get_json() or {}

    is_valid, error = validate_video_create(data)
    if not is_valid:
        return error_response(error, status_code=400)

    try:
        result = VideoService.create_video(data)
        return success_response("영상 등록 성공", result, 201)
    except AppException as e:
        return error_response(e.message, status_code=e.status_code)


@video_bp.route("", methods=["GET"])
@jwt_required()
def get_video_list():
    try:
        result = VideoService.get_video_list()
        return success_response("영상 목록 조회 성공", result)
    except AppException as e:
        return error_response(e.message, status_code=e.status_code)


@video_bp.route("/<int:video_id>", methods=["GET"])
@jwt_required()
def get_video_detail(video_id):
    try:
        result = VideoService.get_video_detail(video_id)
        return success_response("영상 상세 조회 성공", result)
    except AppException as e:
        return error_response(e.message, status_code=e.status_code)


@video_bp.route("/member/<int:member_id>", methods=["GET"])
@jwt_required()
def get_member_videos(member_id):
    try:
        result = VideoService.get_member_videos(member_id)
        return success_response("회원별 영상 조회 성공", result)
    except AppException as e:
        return error_response(e.message, status_code=e.status_code)


@video_bp.route("/<int:video_id>", methods=["PUT"])
@jwt_required()
def update_video(video_id):
    data = request.get_json() or {}

    is_valid, error = validate_video_update(data)
    if not is_valid:
        return error_response(error, status_code=400)

    try:
        result = VideoService.update_video(video_id, data)
        return success_response("영상 수정 성공", result)
    except AppException as e:
        return error_response(e.message, status_code=e.status_code)


@video_bp.route("/<int:video_id>", methods=["DELETE"])
@jwt_required()
def delete_video(video_id):
    try:
        result = VideoService.delete_video(video_id)
        return success_response("영상 삭제 성공", result)
    except AppException as e:
        return error_response(e.message, status_code=e.status_code)