from typing import Any

from fastapi import Depends
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.datastore import postgres_session_provider
from backend.app.service.base import BaseService
from backend.app.model.employee import Employee


def get_employee_service(
        session: AsyncSession = Depends(postgres_session_provider),
):
    return EmployeeService(session)


class EmployeeService(BaseService):
    model = Employee

    async def get_employee_by_filters(self, filters: dict[str, Any]):
        query = select(self.model)
        conditions = []
        string_param = filters.get("string")
        conditions.append(
            or_(
                self.model.first_name.ilike(f"%{string_param}%"),
                self.model.lastname.ilike(f"%{string_param}%"),
                self.model.surname.ilike(f"%{string_param}%"),
                self.model.phone_number.ilike(f"%{string_param}%"),
            )
        )
        age_from_param = filters.get("age_from")
        age_to_param = filters.get("age_to")
        conditions.append(
            and_(
            self.model.age >= age_from_param,
            self.model.age <= age_to_param
            )
        )
        employee_sex_param = filters.get("sex")
        if employee_sex_param and employee_sex_param != "Все":
            conditions.append(
                self.model.sex == employee_sex_param
            )

        query = query.filter(*conditions)
        result = await self.session.execute(query)

        return result.scalars().all()
