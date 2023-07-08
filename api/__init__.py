from fastapi import APIRouter
from api.auth import auth_router
from api.post import post_router


router = APIRouter(
    prefix="/api",
)


router.include_router(auth_router)
router.include_router(post_router)
