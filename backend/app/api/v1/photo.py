from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse

from backend.app.core.exception import NotFoundException
from backend.app.schema.photo import PhotoResponseSchema
from backend.app.service.photo import PhotoService, get_photo_service

BASE_PREFIX = "/photo"

router = APIRouter(
    prefix=BASE_PREFIX,
)


@router.get(
    "/{photo_id}",
    response_model=PhotoResponseSchema,
)
async def get_photo_by_id(
        photo_id: int,
        photo_service: PhotoService = Depends(get_photo_service),
):
    photo = await photo_service.retrieve_one_by_id(photo_id)
    if not photo:
        raise NotFoundException
    return photo


@router.get(
    "/{photo_id}/file",
)
async def get_photo_file(
        photo_id: int,
        photo_service: PhotoService = Depends(get_photo_service),
):
    photo_path = await photo_service.retrieve_file_path_by_id(photo_id)
    if not photo_path:
        raise NotFoundException
    return FileResponse(photo_path)

@router.delete(
    "/{photo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_photo(
        photo_id: int,
        photo_service: PhotoService = Depends(get_photo_service),
):
    photo = await photo_service.delete_file(photo_id)
    if photo:
        return photo
    raise NotFoundException
