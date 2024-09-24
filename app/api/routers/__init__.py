# app/api/routers/__init__.py

# 如果你需要从这个层级直接导出 v1 路由器，可以这样写：
from app.api.routers.v1 import router as v1_router

# 如果你将来添加了其他版本的路由器，也可以在这里导入
# 例如：
# from .v2 import router as v2_router

# 如果你想在这个层级创建一个组合了所有版本的主路由器，可以这样做：
# from fastapi import APIRouter
#
# main_router = APIRouter()
# main_router.include_router(v1_router, prefix="/v1")
# # 如果有 v2，可以这样添加：
# # main_router.include_router(v2_router, prefix="/v2")

# 然后你可以选择导出这个主路由器
# __all__ = ["main_router"]

# 或者，如果你只想导出各个版本的路由器，可以这样写：
__all__ = ["v1_router"]
