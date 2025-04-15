from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, blog, files, settings, images

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(blog.router, prefix="/blog", tags=["blog"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(images.router, prefix="/images", tags=["images"]) 