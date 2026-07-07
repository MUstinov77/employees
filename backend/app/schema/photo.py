from pydantic import BaseModel


class PhotoResponseSchema(BaseModel):
    id: int
    file_path: str
    employee_id: int