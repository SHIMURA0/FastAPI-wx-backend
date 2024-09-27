# /app/api/routers/WeChat/__init__.py

from fastapi import APIRouter
from .v1 import router as v1_router  # 导入 v1 路由

router = APIRouter()

# 包含 WeChat v1 路由
router.include_router(v1_router, prefix="/v1", tags=["WeChat V1"])

# 添加一个 wechat API 的根路由
@router.get("/", tags=["root"])
async def read_wechat_root():
    return {"message": "Welcome to WeChat API !"}
