from fastapi import APIRouter, Depends, HTTPException

from schemas.location import Location
from service.file_service import file_service

router = APIRouter()


@router.get("/media_file", response_model=Location)
def get_media_file_upload_location(
        ext: str
) -> Location:
    # todo 1. 토큰 검증
    user_id = "test_user_01"

    url = file_service.get_media_file_upload_url(user_id=user_id, ext=ext)
    location = Location(**{"url": url})
    return location
