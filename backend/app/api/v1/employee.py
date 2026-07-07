import os


from fastapi import APIRouter, Depends, status, UploadFile, File, Response, Request

from backend.app.core.exception import NotFoundException
from backend.app.model.photo import Photo
from backend.app.schema.employee import EmployeeCreateSchema, EmployeeResponseSchema, EmployeeUpdateSchema
from backend.app.service.employee import EmployeeService, get_employee_service
from backend.app.service.photo import PhotoService, get_photo_service

BASE_PREFIX = "/employee"

router = APIRouter(
    prefix=BASE_PREFIX,
    tags=["employee"],
)

@router.get(
    "/",
    response_model=list[EmployeeResponseSchema],
)
async def get_employees(
        request: Request,
        employee_service: EmployeeService = Depends(get_employee_service),
):
    employees = await employee_service.retrieve_all_by_filters(filters=request.query_params)
    if not employees:
        raise NotFoundException
    return employees


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=EmployeeResponseSchema,
)
async def create_employee(
        data: EmployeeCreateSchema = Depends(EmployeeCreateSchema.as_form),
        file: UploadFile = File(...),
        employee_service: EmployeeService = Depends(get_employee_service),
        photo_service: PhotoService = Depends(get_photo_service)
):
    employee = await employee_service.create(data.model_dump())
    if not employee:
        raise NotFoundException
    _employee_photo = await photo_service.create_file(file, employee.id)
    return employee


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponseSchema,
)
async def get_employee_by_id(
        employee_id: int,
        employee_service: EmployeeService = Depends(get_employee_service),
):
    employee = await employee_service.retrieve_one_by_id(employee_id)
    if not employee:
        raise NotFoundException
    return employee


@router.patch(
    "/{employee_id}",
    response_model=EmployeeResponseSchema,
)
async def update_employee(
        employee_id: int,
        data: EmployeeUpdateSchema = Depends(EmployeeUpdateSchema.as_form),
        file: UploadFile | None = None,
        employee_service: EmployeeService = Depends(get_employee_service),
        photo_service: PhotoService = Depends(get_photo_service),
):
    employee = await employee_service.update(employee_id, data.model_dump())
    if not employee:
        raise NotFoundException
    if file:
        _employee_photo = await photo_service.update_file(file, employee.id)
    return employee


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_employee(
        employee_id: int,
        employee_service: EmployeeService = Depends(get_employee_service),
        photo_service: PhotoService = Depends(get_photo_service),
):
    employee_photo = await photo_service.retrieve_one_by_field(Photo.employee_id, employee_id)
    employee = await employee_service.delete(employee_id)
    if not employee or not employee_photo:
        raise NotFoundException
    os.remove(employee_photo.file_path)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
