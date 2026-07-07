from typing import Any

from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

class BaseService:

    model = None

    def __init__(self, session: AsyncSession):
        self.session = session


    async def retrieve_all_by_filters(self, filters: dict[str, Any] | None = None):
        query = select(self.model)
        if filters:
            pass
        result = await self.session.execute(query)
        return result.scalars().all()

    async def retrieve_one_by_id(self, obj_id: int):
        query = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def retrieve_one_by_field(self, field: Any, field_value: Any):
        query = select(self.model).where(field == field_value)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def create(self, values: dict):
        try:
            record = self.model(**values)
            self.session.add(record)
            await self.session.commit()
            return record
        except SQLAlchemyError:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="Error during create instance")

    async def update(self, obj_id: int, values: dict):
        query = (
            update(self.model).
            values(**values).
            where(self.model.id == obj_id).
            returning(self.model)
        )
        result = await self.session.execute(query)
        return result.scalars().one()

    async def delete(self, obj_id: int):
        query = delete(self.model).where(self.model.id == obj_id).returning(self.model)
        result = await self.session.execute(query)
        return result.scalars().first()
