from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    code: str = Field(
        ...,
        description="用户登录时获取的授权码",
        min_length=1,
        max_length=255,
        examples=["auth_code_123456"]
    )


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(
        ...,
        description="用于刷新访问令牌的刷新令牌",
        min_length=1,
        max_length=255,
        examples=["refresh_token_abcdef123456"]
    )


class TokenResponse(BaseModel):
    access_token: str = Field(
        ...,
        description="用于访问受保护资源的访问令牌",
        min_length=1,
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"]
    )

    refresh_token: str = Field(
        ...,
        description="用于获取新的访问令牌的刷新令牌",
        min_length=1,
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"]
    )

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                # "token_type": "bearer"
            }
        }
