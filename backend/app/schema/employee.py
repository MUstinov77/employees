from datetime import date
from typing import Annotated

from fastapi import Form
from pydantic import BaseModel, computed_field

from backend.app.core.enum.employee import EmployeeSex


class EmployeeCreateSchema(BaseModel):
    first_name: str
    lastname: str
    surname: str | None
    date_of_birth: date
    phone_number: str | None
    sex: EmployeeSex

    @computed_field
    @property
    def age(self) -> int:
        today = date.today()
        age = today.year - self.date_of_birth.year
        return age

    @classmethod
    def as_form(
            cls,
            first_name: Annotated[str, Form(...)],
            lastname: Annotated[str, Form(...)],
            date_of_birth: Annotated[date, Form(...)],
            sex: Annotated[EmployeeSex, Form(...)],
            phone_number: Annotated[str | None, Form(...)] = None,
            surname: Annotated[str | None, Form(...)] = None,
    ):
        return cls(
            first_name=first_name,
            lastname=lastname,
            surname=surname,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            sex=sex
        )


class EmployeeUpdateSchema(BaseModel):
    first_name: str | None
    lastname: str | None
    surname: str | None
    lastname: str | None
    surname: str | None
    date_of_birth: date | None
    phone_number: str | None
    sex: EmployeeSex | None

    @classmethod
    def as_form(
            cls,
            first_name: Annotated[str | None, Form(...)] = None,
            lastname: Annotated[str | None, Form(...)] = None,
            surname: Annotated[str | None, Form(...)] = None,
            date_of_birth: Annotated[date | None, Form(...)] = None,
            phone_number: Annotated[str | None, Form(...)] = None,
            sex: Annotated[EmployeeSex | None, Form(...)] = None
    ):
        return cls(
            first_name=first_name,
            lastname=lastname,
            surname=surname,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            sex=sex
        )


class EmployeeResponseSchema(BaseModel):
    id: int
    first_name: str
    lastname: str
    surname: str | None
    date_of_birth: date
    age: int | None
    phone_number: str | None
    sex: str