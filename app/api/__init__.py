# /app/api/__init__.py

# 导入 FastAPI 的一些核心组件（如果需要）
from fastapi import APIRouter

# 导入 routers 模块
from .routers import router as api_router

# 可以根据需要定义其他功能，比如 API 相关的配置、依赖等

# 类似于导入异常处理、事件处理等
# from .core import my_core_function

# 创建一个主 API 路由器（如果没有在 routers/__init__.py 中创建）
# api_router = APIRouter()

# 这里主要是对 API 进行组织，通常不需要在这个文件中定义路由

