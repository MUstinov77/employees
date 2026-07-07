from typing import TYPE_CHECKING

from datetime import date

from .base import Base
from sqlalchemy import Integer, String, DATE, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

if TYPE_CHECKING:
    from backend.app.model.photo import Photo


class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    first_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    lastname: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    surname: Mapped[str] = mapped_column(
        String,
        nullable=True
    )
    phone_number: Mapped[str] = mapped_column(
        String,
        nullable=True
    )
    date_of_birth: Mapped[date] = mapped_column(
        DATE,
        nullable=False
    )
    age: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
        default=1
    )
    sex: Mapped[str] = mapped_column(
        String(),
        nullable=False,
    )

    photo: Mapped["Photo"] = relationship(
        back_populates="employee",
        cascade="all, delete, delete-orphan",
        lazy="selectin"
    )