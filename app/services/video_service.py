from app.models.video_model import Video
from app.repositories.video_repository import VideoRepository
from app.repositories.member_repository import MemberRepository
from app.common.exceptions import NotFoundException, ValidationException


class VideoService:
    @staticmethod
    def create_video(data):
        member = MemberRepository.get_by_id(data["member_id"])
        if not member:
            raise ValidationException("존재하지 않는 회원입니다.", 404)

        video = Video(
            member_id=data["member_id"],
            title=data["title"],
            original_filename=data["original_filename"],
            saved_filename=data["saved_filename"],
            file_path=data["file_path"],
            file_size=data.get("file_size"),
            duration_sec=data.get("duration_sec"),
            status=data.get("status", "uploaded")
        )

        saved_video = VideoRepository.create_video(video)
        return saved_video.to_dict()

    @staticmethod
    def get_video_list():
        videos = VideoRepository.get_all()
        return [video.to_dict() for video in videos]

    @staticmethod
    def get_video_detail(video_id):
        video = VideoRepository.get_by_id(video_id)
        if not video:
            raise NotFoundException("영상을 찾을 수 없습니다.", 404)

        return video.to_dict()

    @staticmethod
    def get_member_videos(member_id):
        videos = VideoRepository.get_by_member_id(member_id)
        return [video.to_dict() for video in videos]

    @staticmethod
    def update_video(video_id, data):
        video = VideoRepository.get_by_id(video_id)
        if not video:
            raise NotFoundException("영상을 찾을 수 없습니다.", 404)

        if "title" in data:
            video.title = data["title"]
        if "status" in data:
            video.status = data["status"]
        if "duration_sec" in data:
            video.duration_sec = data["duration_sec"]
        if "file_size" in data:
            video.file_size = data["file_size"]

        VideoRepository.save()
        return video.to_dict()

    @staticmethod
    def delete_video(video_id):
        video = VideoRepository.get_by_id(video_id)
        if not video:
            raise NotFoundException("영상을 찾을 수 없습니다.", 404)

        VideoRepository.delete(video)
        return {"deleted_video_id": video_id}