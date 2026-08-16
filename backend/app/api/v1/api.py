from fastapi import APIRouter

from app.modules.users.routes import router as users_router
from app.modules.companies.routes import router as companies_router

api_router = APIRouter()

api_router.include_router(users_router)
api_router.include_router(companies_router)
