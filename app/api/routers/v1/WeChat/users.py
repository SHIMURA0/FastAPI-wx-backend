"""
app/api/routers/v1/users.py

This module defines the API routes related to user operations for version 1 of the API.
It includes endpoints for retrieving user information based on authentication tokens.

Main Components:
- Router setup for user-related endpoints: Defines the routes for accessing user services.
- Dependency injection for user authentication and services: Utilizes FastAPI's dependency
  injection to integrate authentication mechanisms and user services.
- An endpoint to retrieve user information: Provides functionality to fetch and return user data
  using validated access tokens.

Integrations:
- Works in conjunction with authentication services, user services, and database models to
  ensure secure and streamlined access to user data.
- Relies on FastAPI for routing and dependency management.

Usage Example:
The module can be used to set up API routes related to user management, particularly for
retrieving information about the authenticated user, like so:

    @router.get("/user_info", response_model=UserInfo)
    async def get_user_info(
            current_user: Annotated[str, Depends(get_current_user)],
            user_service: Annotated[UserService, Depends(get_user_service)]
    ) -> Optional[UserInfo]:
        ...

Dependencies:
- FastAPI: For setting up routes and dependency injection.
- Pydantic: For validating and serializing user data models.
- User services: For handling business logic and database interactions related to users.

This file is part of the FastAPI application structure, organized under the version 1 API
directory, indicating it is intended for handling user-related HTTP requests in this API version.
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Header
)
from typing import (
    Annotated,
    Optional, Dict, Any
)
from app.api.dependencies import get_current_user
from app.core import verify_token
from app.core.config import settings
from app.schemas.WeChat.user import NameUpdate as UserNameSchema
from app.services.WeChat.users import (
    get_user_service,
    UserService
)
from app.schemas.WeChat.user import UserInfo

router = APIRouter()


@router.get("/get_user_info", response_model=UserInfo)
async def get_user_info(
        current_user: Annotated[str, Depends(get_current_user)],
        user_service: Annotated[UserService, Depends(get_user_service)]
) -> Optional[UserInfo]:
    """
    Retrieve user information based on the provided access token.

    This endpoint retrieves and returns user information as a Pydantic model,
    using the access token provided by the client to identify the current user.

    Args:
        current_user (str): The current user's openid, derived from the validated
            access token.
        user_service (UserService): An instance of UserService for performing
            database operations to fetch user data.

    Returns:
        Optional[UserInfo]: A Pydantic UserInfo model containing user's real_name
            and openid if the user exists; returns None if the user is not found.

    Raises:
        HTTPException: If no user is found in the database, raises a 404 Not Found error.

    Process:
        1. The client provides an access token to the /user_info endpoint.
        2. The token is verified by the get_current_user dependency to obtain the user's openid.
        3. UserService uses the openid to fetch information from the database.
        4. Return the user information as a UserInfo model.
    """
    # Attempt to retrieve user information using the provided openid
    user_info: Optional[UserInfo] = await user_service.get_user_info(current_user)

    # If no user information is found, raise a 404 Not Found exception
    if not user_info:
        raise HTTPException(status_code=404, detail="User not found")

    # Return the user information if found
    return user_info


oauth2_scheme = settings.OAUTH2_SCHEME


@router.put("/update_user_name")
async def update_user_info(
        user_service: Annotated[UserService, Depends(get_user_service)],
        user_real_name: UserNameSchema,
        token: str = Depends(oauth2_scheme)
        # authorization: str = Header(...),
) -> Dict[str, str]:
    # token: str = authorization.split(" ")[1]
    payload: Dict[str, Any] = await verify_token(token, 'access')
    openid: str = payload.get("sub")
    real_name: str = user_real_name.real_name
    await user_service.update_user(openid, real_name)
    return {"message": "User's real name has been successfully recorded"}
