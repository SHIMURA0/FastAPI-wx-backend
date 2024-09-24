"""
app/services/auth.py

This module provides authentication services for handling user authentication
via WeChat's API and generating access and refresh tokens.

Classes:
    AuthService: Provides methods to authenticate users with a WeChat code,
    retrieve or create a user in the database, and generate authentication tokens.

Functions:
    get_auth_service(user_repo: Annotated[UserRepository, Depends(get_user_repository)]) -> AuthService:
        Retrieves an instance of the AuthService with injected dependencies.

Usage:
    This module is intended to be used as part of the authentication flow within a
    FastAPI application, where it interacts with external WeChat services and internal
    user management systems to authenticate users and issue tokens.

    Example:
        auth_service = await get_auth_service(user_repo)
        tokens = await auth_service.authenticate_user(code="some_wechat_code")

Dependencies:
    - FastAPI for dependency injection.
    - httpx for making asynchronous HTTP requests.
    - app/core/security for token generation utilities.
    - app/crud.user for user repository interactions.
    - app.schemas.user for user data schema.
    - app.models.user for the user model used in the database.
    - app.api.dependencies.user for retrieving repository dependencies.
"""

from typing import (
    Annotated,
    Self,
    Dict,
    Optional
)
import httpx
from fastapi import Depends
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token
)
from app.crud.WeChat.user import UserRepository
from app.api.dependencies import get_user_repository
from app.schemas.WeChat.user import UserInfo
from app.models.WeChat.user import User as UserModel


class AuthService:
    """Service class responsible for user authentication and token generation."""

    def __init__(self, user_repo: UserRepository) -> None:
        """Initializes AuthService with a UserRepository for user data operations.

        Args:
            user_repo: An instance of UserRepository to interact with user data.
        """
        self.user_repo = user_repo

    async def authenticate_user(
            self,
            code: str
    ) -> Dict[str, str]:
        """Authenticates a user using a WeChat code and generates access and refresh tokens.

        Args:
            code: A string representing the WeChat code used for authentication.

        Returns:
            A dictionary containing the access and refresh tokens.

        Raises:
            ValueError: If obtaining the openid from WeChat fails.
        """
        # Step 1: Get WeChat openid
        openid: str = await self.get_wechat_openid(code)

        # Step 2: Retrieve user from database using openid
        user: Optional[UserModel] = await self.user_repo.get_by_openid(openid)

        # If user doesn't exist, create a new user
        if not user:
            # Create a new user with empty real_name and the retrieved openid
            user = await self.user_repo.create(
                UserInfo(real_name="", openid=openid)
            )

        # Step 3: Generate tokens
        # Create access token with user's openid as the subject
        access_token: str = await create_access_token(data={"sub": str(user.openid)})
        # Create refresh token with user's openid as the subject
        refresh_token: str = await create_refresh_token(data={"sub": str(user.openid)})

        # Step 4: Return tokens
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    @staticmethod
    async def get_wechat_openid(
            code: str
    ) -> str:
        """Fetches the WeChat openid using a provided code.

        Args:
            code: The WeChat login temporary code used for session conversion.

        Returns:
            The openid as a string obtained from WeChat.

        Raises:
            ValueError: If the WeChat API returns an error.
        """
        # WeChat API endpoint for code to session conversion
        url = "https://api.weixin.qq.com/sns/jscode2session"

        # Prepare request parameters
        params = {
            "appid": settings.WECHAT_APP_ID,  # Your WeChat App ID
            "secret": settings.WECHAT_APP_SECRET,  # Your WeChat App Secret
            "js_code": code,  # The temporary code from WeChat login
            "grant_type": "authorization_code"  # Fixed value as per WeChat API documentation
        }

        # Use httpx for asynchronous HTTP requests
        async with httpx.AsyncClient() as client:
            # Send GET request to WeChat API
            response = await client.get(url, params=params)
            # Parse JSON response
            data = response.json()

        # Check for errors in the API response
        if 'errcode' in data:
            # If an error is present, raise a ValueError with the error message
            raise ValueError(f"Failed to get openid: {data.get('errmsg', 'Unknown error')}")

        # Return the openid if successful
        return data['openid']

    @classmethod
    async def create(
            cls,
            user_repo: UserRepository
    ) -> Self:
        """Factory method to create an instance of AuthService.

        Args:
            user_repo: An instance of UserRepository.

        Returns:
            An instance of AuthService.
        """
        return cls(user_repo)


async def get_auth_service(
        user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> AuthService:
    """Creates and provides an instance of AuthService with dependencies injected.

    Args:
        user_repo: The UserRepository dependency injected by FastAPI.

    Returns:
        An initialized instance of AuthService.
    """
    return await AuthService.create(user_repo)
