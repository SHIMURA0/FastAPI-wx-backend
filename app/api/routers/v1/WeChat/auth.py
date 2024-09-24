"""
app/api/routers/v1/auth.py

This module defines the authentication-related API routes for version 1 of the API.
It includes endpoints for user login and token refreshing, fundamental for maintaining security
and session continuity in the application.

Main Components:
- Router setup for authentication endpoints: Defines API routes to manage user authentication processes.
- Token-based authentication and session management: Manages the creation and refresh of access
  and refresh tokens via secure APIs.

Endpoint Details:
- POST /login: Handles login requests by authenticating users with a WeChat login code.
  It returns JWT access and refresh tokens upon successful login, enabling session management.
- POST /refresh_token: Provides functionality to renew expired access tokens using valid refresh tokens,
  ensuring continuous user access without re-authentication.

Integrations:
- Utilizes authentication schemas and security services within the application to handle login and token management robustly.
- Works in tandem with the app's AuthService to authenticate users and refresh tokens seamlessly.

Usage Example:
The primary interaction involves user authentication via login endpoints and refreshing session tokens:

    @router.post("/login", response_model=TokenResponse)
    async def login(
            login_request: LoginRequest,
            auth_service: Annotated[AuthService, Depends(get_auth_service)]
    ) -> Dict[str, str]:
        ...

Dependencies:
- FastAPI: For setting up HTTP endpoints and handling request dependencies.
- Pydantic: Utilized for validating and serializing incoming login and token refresh requests.
- Application Services: Relies on AuthService and core security functions to handle business logic related to authentication.

This module is a crucial element of the FastAPI application, facilitating secure user login processes and maintaining session validity through effective token management.
"""

from fastapi import APIRouter, HTTPException
from app.schemas.WeChat.auth import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest
)
from app.services.WeChat.auth import (
    AuthService,
    get_auth_service
)
from app.core.security import refresh_tokens
from fastapi import Depends
from typing import (
    Dict,
    Annotated
)

router = APIRouter()


@router.post(path="/login", response_model=TokenResponse)
async def login(
        login_request: LoginRequest,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> Dict[str, str]:
    """
    Handle user login requests.

    This endpoint processes a login request containing a WeChat login code,
    authenticates the user, and returns access and refresh tokens.

    Args:
        login_request (LoginRequest): An object containing the WeChat login code.
            This code is typically obtained from the WeChat OAuth process.
        auth_service (AuthService): The instance of AuthService automatically
            injected by FastAPI's dependency system to handle authentication logic.

    Returns:
        Dict[str, str]: A dictionary comprising the access token, refresh token,
                        and token type as specified by TokenResponse.

    Raises:
        HTTPException: Raised for authentication errors with status 400.

    Example:
        Request:
            POST /login
            {
                "code": "WeChat_OAuth_Code_Here"
            }
    """
    try:
        # Attempt to authenticate the user using the provided WeChat temporary code
        tokens: Annotated[
            Dict[str, str],
            "a dictionary containing access token and refresh token"
        ] = await auth_service.authenticate_user(login_request.code)

        return tokens

    except ValueError as e:
        # If a ValueError is raised during authentication, convert it to an HTTP 400 error
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/refresh_token", response_model=TokenResponse)
async def refresh_token(
        refresh_request: RefreshTokenRequest,
) -> Dict[str, str]:
    """
    Endpoint to refresh an access token using a valid refresh token.

    Args:
        refresh_request (RefreshTokenRequest): An object containing the refresh token from the client.

    Returns:
        Dict[str, str]: A dictionary with the new access token and possibly
                        a new refresh token, formatted per TokenResponse.

    Raises:
        HTTPException:
            - HTTP 400: If the refresh token is invalid.
            - HTTP 401: If the refresh token is expired or not found.
            - HTTP 500: For any unexpected server errors.

    Notes:
        - Ensure that your tokens are securely stored client-side to maintain valid sessions.
    """
    try:
        # Attempt to refresh the tokens using the provided refresh token
        new_tokens: Annotated[
            Dict[str, str],
            "a dictionary containing access token and refresh token"
        ] = await refresh_tokens(refresh_request.refresh_token)

        # Refresh successful, return new tokens
        return new_tokens

    except ValueError as e:
        # If a ValueError is raised during the refresh process, convert it to an HTTP 400 error
        # This could happen if the token format is invalid
        raise HTTPException(status_code=400, detail=f"Invalid token format: {str(e)}")

    except HTTPException as e:
        # Re-raise HTTP exceptions, typically used for invalid or expired refresh tokens
        # This maintains the original status code and error message
        raise

    except Exception as e:
        # Catch any unexpected errors and return a 500 Internal Server Error
        # This is a fallback for any unforeseen issues
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
