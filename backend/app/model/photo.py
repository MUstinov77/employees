import os
from typing import TYPE_CHECKING

from sqlalchemy.event import listens_for

from .base import Base
from sqlalchemy import Integer, String, DATE, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

if TYPE_CHECKING:
    from backend.app.model.employee import Employee


class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    file_path: Mapped[str] = mapped_column(
        String,
    )

    employee_id: Mapped[int] = mapped_column(
        ForeignKey(
            "employees.id",
            ondelete="CASCADE",
        ),
    )

    employee: Mapped["Employee"] = relationship(
        back_populates="photo",
        lazy="selectin"
    )

    __table_args__ = (
        UniqueConstraint(
            "employee_id",
            "id",
            name="unique_employee_photo_id",
        ),
    )