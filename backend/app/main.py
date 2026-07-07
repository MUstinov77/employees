from starlette.templating import Jinja2Templates

from backend.app.app_factory import create_app
from backend.app.core.exception import NotFoundException
from backend.app.service.employee import EmployeeService, get_employee_service

from fastapi import Request, Depends

templates = Jinja2Templates(directory="app/templates")

app = create_app()


@app.get("/")
async def root(
        request: Request,
        employee_service: EmployeeService = Depends(get_employee_service),
):
    employees = await employee_service.retrieve_all_by_filters(request.query_params)
    pages = len(employees) // 20
    return templates.TemplateResponse(
        request,
        name="employees/list.html",
        context={
            "request": request,
            "employees": employees,
            "pages": pages,
            "page": 1,
        }
    )

# @app.get("/employees/search")
# async def employee_search(
#         request: Request,
#         employee_service: EmployeeService = Depends(get_employee_service),
# ):
#     employees = await employee_service.retrieve_all_by_filters(filters=request.query_params)
#

@app.get("/employees/create")
async def create_employee(request: Request):
    return templates.TemplateResponse(
        request,
        name="employees/create.html",
        context={
            "request": request
        }
    )

@app.get("/employees/{employee_id}/edit")
async def employee_edit(
        employee_id: int,
        request: Request,
        employee_service: EmployeeService = Depends(get_employee_service),
):
    employee = await employee_service.retrieve_one_by_id(employee_id)
    if not employee:
        raise NotFoundException
    return templates.TemplateResponse(
        request,
        name="employees/edit.html",
        context={
            "request": request,
            "employee": employee,
            "photo_path": employee.photo.id
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)