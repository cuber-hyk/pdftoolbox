from fastapi import APIRouter
from app.api.v1.endpoints import tools, files, jobs

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(tools.router, prefix='/tools', tags=['tools'])
api_router.include_router(files.router, prefix='/files', tags=['files'])
api_router.include_router(jobs.router, prefix='/jobs', tags=['jobs'])
