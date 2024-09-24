from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import api_router
from app.db import (
    init_db,
    close_db
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时的代码
    await init_db()
    yield
    # 关闭时的代码
    await close_db()


app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1/wechat")


@app.get("/")
async def root():
    return {"message": "W"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
