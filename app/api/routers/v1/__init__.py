# app/api/routers/v1/__init__.py

from fastapi import APIRouter

# 导入所有子路由器
from app.api.routers.v1.WeChat.instruments import router as instruments_router
from app.api.routers.v1.WeChat.rooms import router as rooms_router
from app.api.routers.v1.WeChat.users import router as users_router
from app.api.routers.v1.WeChat.auth import router as auth_router

# 如果还有其他路由器，继续导入...

# 创建主路由器
router = APIRouter()

# 包含所有子路由器
router.include_router(instruments_router, prefix="/instruments", tags=["Instruments"])
router.include_router(rooms_router, prefix="/rooms", tags=["Rooms"])
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])


# 如果还有其他路由器，继续包含...

# 可选：添加一个 v1 API 的根路由
@router.get("/", tags=["root"])
async def read_v1_root():
    return {"message": "Welcome to API v1"}
