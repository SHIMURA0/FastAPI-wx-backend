# app/api/__init__.py

from fastapi import APIRouter
from .routers import v1_router

# 创建一个主 API 路由器
api_router = APIRouter()

# 包含 v1 版本的路由
api_router.include_router(v1_router, prefix="/v1")

# 如果你有其他版本的 API，也可以在这里包含
# 例如：
# from .routers.v2 import router as v2_router
# api_router.include_router(v2_router, prefix="/v2")
