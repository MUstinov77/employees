import os
import uuid
from mimetypes import guess_extension, guess_type

from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.datastore import postgres_session_provider
from backend.app.core.configuration import settings
from backend.app.service.base import BaseService

from backend.app.model.photo import Photo


def get_photo_service(
        session: AsyncSession = Depends(postgres_session_provider)
):
    return PhotoService(session)


class PhotoService(BaseService):

    model = Photo

    async def retrieve_file_path_by_id(self, obj_id: int):
        query = select(self.model.file_path).where(self.model.id == obj_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def create_file(self, file, employee_id: int):
        try:
            if file.size > settings.MAX_PHOTO_SIZE_KB * 1024:
                raise HTTPException(status_code=400, detail="File too large")
            mime_type, _ = guess_type(file.filename)
            if mime_type not in ("image/png", "image/jpg", "image/jpeg"):
                raise HTTPException(status_code=400, detail="File type not supported")

            file_id = uuid.uuid4()
            file_extension = guess_extension(mime_type)
            new_file_name = f"{file_id}{file_extension}"
            file_path = os.path.join(settings.PHOTO_DIRECTORY_PATH, new_file_name)

            photo_create_data = {
                "file_path": file_path,
                "employee_id": employee_id,
            }

            photo_create_data.update(photo_create_data)
            photo = await self.create(photo_create_data)
            file_content = await file.read()
            with open(photo.file_path, "wb") as f:
                f.write(file_content)
        except Exception:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="Photo creation failed")
        return photo

    async def update_file(self, file, employee_id: int):
            try:
                if file.size > settings.MAX_PHOTO_SIZE_KB * 1024:
                    raise HTTPException(status_code=400, detail="File too large")
                mime_type, _ = guess_type(file.filename)
                if mime_type not in ("image/png", "image/jpg", "image/jpeg"):
                    raise HTTPException(status_code=400, detail="File type not supported")
                employee_photo = await self.retrieve_one_by_field(self.model.employee_id, employee_id)
                file_content = await file.read()
                with open(employee_photo.file_path, "wb") as f:
                    f.write(file_content)
                await self.session.refresh(employee_photo)
            except Exception:
                await self.session.rollback()
                raise HTTPException(status_code=400, detail="Photo creation failed")
            return employee_photo

    async def delete_by_employee_id(self, employee_id: int):
        query = delete(self.model).where(self.model.employee_id == employee_id).returning(self.model)
        result = await self.session.execute(query)
        record = result.scalars().one()
        return record


    async def delete_file(self, employee_id: int):
        try:
            photo = await self.delete_by_employee_id(employee_id)
            print(photo)
            os.remove(photo.file_path)
            await self.session.commit()
        except SQLAlchemyError:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="Photo deletion failed")
        return photo



