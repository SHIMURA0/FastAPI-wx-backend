# app/api/routers/WeChat/v1/__init__.py
from fastapi import APIRouter
from .auth import router as auth_router
from .instruments import router as instruments_router
from .rooms import router as rooms_router
from .users import router as users_router

router = APIRouter()

# 包含不同的子路由器
router.include_router(auth_router, prefix="/auth", tags=["WeChat Auth"])
router.include_router(instruments_router, prefix="/instruments", tags=["WeChat Instruments"])
router.include_router(rooms_router, prefix="/rooms", tags=["WeChat Rooms"])
router.include_router(users_router, prefix="/users", tags=["WeChat Users"])


# 添加一个 v1 API 的根路由
@router.get("/", tags=["root"])
async def read_v1_root():
    return {"message": "Welcome to API WeChat v1 !"}
