from fastapi import APIRouter
from backend.app.api.v1.employee import router as employee_router
from backend.app.api.v1.photo import router as photo_router

api_router = APIRouter(
    prefix="/api",
    tags=["api"],
)

api_router.include_router(employee_router)
api_router.include_router(photo_router)

@api_router.get("/")
async def health_check():
    return {"status": "ok"}