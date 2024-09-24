# app/api/dependencies/user.py

from fastapi import Depends, HTTPException
from app.core import verify_token
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_db
from app.crud.WeChat.user import UserRepository as AsyncUserRepository
from typing import Dict, Any

# Use the OAUTH2_SCHEME from settings instead of creating a new one
oauth2_scheme = settings.OAUTH2_SCHEME


async def get_current_user(
        token: str = Depends(oauth2_scheme)
) -> str:
    """Verify an accessToken from the frontend and return the corresponding user's openid"""
    payload: Dict[str, Any] = await verify_token(token, expected_type="access")
    openid: str = payload.get("sub")
    if openid is None:
        raise HTTPException(status_code=401, detail="Token contains no valid openid")
    return openid


async def get_user_repository(
        db: AsyncSession = Depends(get_async_db)
) -> AsyncUserRepository:
    return AsyncUserRepository(db)
