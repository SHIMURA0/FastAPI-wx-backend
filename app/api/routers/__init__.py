# app/api/routers/__init__.py

from fastapi import APIRouter

# 创建一个主路由器
router = APIRouter()

# 导入不同的路由模块
from .WeChat import router as wechat_router  # WeChat 路由
# TODO: from .React import router as react_router  # React 路由

# 包含 WeChat 路由
router.include_router(wechat_router, prefix="/wechat", tags=["WeChat"])
# 包含 React 路由
# TODO: router.include_router(react_router, prefix="/react", tags=["React"])

# 添加一个routers的根路由
@router.get("/", tags=["root"])
async def read_router_root():
    return {"message": "Welcome to WeChat and React routers !"}


