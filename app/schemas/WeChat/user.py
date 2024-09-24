from pydantic import BaseModel, Field
from typing import Optional


class UserInfo(BaseModel):
    real_name: Optional[str] = Field(
        None,
        description="用户的真实姓名",
        max_length=100,
        examples=["张三"]
    )
    openid: str = Field(
        ...,
        description="用户的唯一标识符，通常由认证服务提供",
        min_length=1,
        max_length=255,
        examples=["oi_12345abcde"]
    )

    class Config:
        schema_extra = {
            "example": {
                "real_name": "张三",
                "openid": "oi_12345abcde"
            }
        }


class NameUpdate(BaseModel):
    real_name: str = Field(
        ...,
        description="用户更新的真实姓名",
        min_length=1,
        max_length=100,
        examples=["李四"]
    )

    class Config:
        schema_extra = {
            "example": {
                "real_name": "李四"
            }
        }
