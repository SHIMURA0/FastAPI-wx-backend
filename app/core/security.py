# /app/core/security.py

"""
security.py: Token and Authentication Utilities

This module provides functions for handling JWT (JSON Web Token) creation and management,
as well as utilities for interacting with WeChat's authentication system.

Functions:
1. create_access_token(data: Dict[str, Any], expires_delta: timedelta = None) -> str
   Creates a time-limited JWT access token for user authentication.

2. create_refresh_token(data: Dict[str, Any], expires_delta: timedelta = None) -> str
   Creates a JWT refresh token with a longer expiry period for obtaining new access tokens.

3. timed_lru_cache(seconds: int, maxsize: int = 128)
   A decorator that provides a timed LRU (Least Recently Used) cache for functions.

4. get_wechat_access_token() -> str
   Retrieves and caches the WeChat access token, using the timed LRU cache decorator.

This module is part of the authentication and security system for the FastAPI-WeChat application.
It handles token creation, caching, and interaction with external authentication services (WeChat).

Note: Proper error handling and logging are implemented throughout to ensure robust operation
and easier debugging.

Constants:
- WECHAT_TOKEN_URL: The URL for obtaining WeChat access tokens.
- TOKEN_GRANT_TYPE: The grant type used in WeChat token requests.

Dependencies:
- datetime: For handling token expiration times.
- fastapi: For raising HTTP exceptions.
- jose: For JWT encoding and decoding.
- requests: For making HTTP requests to WeChat's API.
- functools: For implementing the timed LRU cache.
- logging: For logging errors and important information.

Configuration:
- Settings are imported from app.core.config, ensuring centralized configuration management.

Usage:
This module should be imported and used in other parts of the application that require
token creation, validation, or interaction with WeChat's authentication system.
"""

from datetime import (
    datetime,
    timedelta,
    timezone
)
from fastapi import HTTPException
from jose import jwt, JWTError
from typing import Dict, Any
import requests
from app.core.config import settings
from functools import lru_cache
import time
import logging
from functools import wraps

# 常量定义
WECHAT_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
TOKEN_GRANT_TYPE = "client_credential"
logger = logging.getLogger(__name__)


async def create_access_token(
        data: Dict[str, Any],
        expires_delta: timedelta = None
) -> str:
    """
    Create a time-limited JWT (JSON Web Token) access token.

    This function encodes crucial information (typically the user's OpenID) into a JWT
    that will be sent to the frontend for authentication purposes.

    Args:
        data (Dict[str, Any]): A dictionary containing the data to be encoded into the token.
                               Typically, includes user identification information.
                               Expected format: {"sub": openid}
        expires_delta (timedelta, optional): A timedelta object specifying the token's validity period.
                                             If not provided, a default expiration time will be used.

    Returns:
        str: A string representing the encoded JWT token.

    Raises:
        HTTPException: If token creation fails, an HTTPException with a 500 status code is raised.
    """

    # Create a copy of the data to avoid modifying the original
    to_encode: Dict[str, Any] = data.copy()

    # Set the token's expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # If no expiration time is provided, use the default value from settings
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add expiration time and token type to the data to be encoded
    to_encode.update(
        {
            "exp": expire,
            "type": "access"
        }
    )

    try:
        # Use the JWT library to encode the data and create the token
        # is signed using the secret key and specified algorithm from settings
        encoded_jwt: str = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt
    except JWTError as e:
        # If an error occurs during token creation, raise an HTTP exception
        # This prevents sensitive error details from being exposed to the client
        raise HTTPException(status_code=500, detail=f"Failed to create access token: {str(e)}")


async def create_refresh_token(
        data: Dict[str, Any],
        expires_delta: timedelta = None
) -> str:
    """
    Create a JWT (JSON Web Token) refresh token.

    Refresh tokens are used to obtain new access tokens after the original access token has expired.
    They typically have a longer validity period compared to access tokens.

    Args:
        data (Dict[str, Any]): A dictionary containing the data to be encoded into the token.
                               This usually includes user identification information such as user ID.
        expires_delta (timedelta, optional): A timedelta object specifying the token's validity period.
                                             If not provided, a default expiration time will be used.

    Returns:
        str: The encoded JWT refresh token.

    Raises:
        HTTPException: If token creation fails, an HTTPException with a 500 status code is raised.
    """

    # Create a copy of the input data to avoid modifying the original
    to_encode = data.copy()

    # Set the token's expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # If no expiration time is provided, use the default value from settings
        # Note that refresh tokens typically have a longer validity period, hence using days as the unit
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    # Add expiration time and token type to the data to be encoded
    # Explicitly specify the type as "refresh" to distinguish it from access tokens
    to_encode.update(
        {
            "exp": expire,
            "type": "refresh"
        }
    )

    try:
        # Use the JWT library to encode the data and create the token
        # The same secret key and algorithm are used as for access tokens, but the content and purpose differ
        encoded_jwt: str = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt
    except JWTError as e:
        # If an error occurs during token creation, raise an HTTP exception
        # This prevents sensitive error details from being exposed to the client
        raise HTTPException(status_code=500, detail=f"Failed to create refresh token: {str(e)}")


def timed_lru_cache(seconds: int, maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = seconds
        func.expiration = time.time() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if time.time() >= func.expiration:
                func.cache_clear()
                func.expiration = time.time() + func.lifetime
            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


@timed_lru_cache(seconds=7000)  # 设置缓存时间为7000秒，略小于微信token的有效期
def get_wechat_access_token() -> str:
    """
    获取微信的访问令牌。使用带有时间限制的缓存，避免频繁请求。

    Returns:
        str: 微信的访问令牌。

    Raises:
        HTTPException: 如果无法获取访问令牌则抛出此异常。
    """
    url = f"{WECHAT_TOKEN_URL}?grant_type={TOKEN_GRANT_TYPE}&appid={settings.WECHAT_APP_ID}&secret={settings.WECHAT_APP_SECRET}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'access_token' in data:
            return data['access_token']
        else:
            raise ValueError("Access token not found in response")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Failed to connect to WeChat API: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse WeChat response: {str(e)}")


async def verify_token(
        token: str,
        expected_type: str
) -> Dict[str, Any]:
    """
    This function verifies a JWT token, ensuring it is valid and of the expected type.

    Parameters:
    - token: A string representing the JWT token to be verified.
    - expected_type: A string denoting the expected type of the token (e.g., "access" or "refresh").

    Returns:
    - A dictionary containing the decoded payload if verification is successful.

    Raises:
    - HTTPException: If the token is invalid, expired, or does not match the expected type.
    """
    try:
        # Attempt to decode the JWT token using the secret key and algorithm specified in settings
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,  # Secret key used for decoding the token
            algorithms=[settings.JWT_ALGORITHM]  # Algorithm used in decoding, typically 'HS256'
        )

        # Check if the token's 'type' matches the expected type
        if payload.get("type") != expected_type:
            # Raise an HTTP 401 Unauthorized exception if the token type does not match
            raise HTTPException(
                status_code=401,  # HTTP status code for unauthorized access
                detail=f"Invalid token type. Expected {expected_type}."  # Explanation of the error
            )

        # If everything is correct, return the decoded payload
        return payload

    except JWTError:
        # If any error occurs during decoding, raise an HTTP 401 Unauthorized exception
        raise HTTPException(status_code=401, detail="Invalid or expired token")


async def refresh_tokens(
        refresh_token: str
) -> Dict[str, str]:
    """
    Refresh the access and refresh tokens.

    This function takes a refresh token, verifies it, and if valid, generates new access and refresh tokens.

    Args:
        refresh_token (str): The refresh token sent from the client.

    Returns:
        Dict[str, str]: A dictionary containing the new access and refresh tokens.

    Raises:
        HTTPException: If the refresh token is invalid or if there's an unexpected error.
    """
    try:
        # Verify and decode the refresh token sent from the frontend
        # This step ensures the token is valid, not expired, and of the correct type
        payload = await verify_token(refresh_token, expected_type="refresh")

        # Extract the open_id (user identifier) from the token payload
        # The 'sub' claim typically contains the subject of the token, which is usually the user ID
        open_id = payload.get("sub")

        # If the payload does not contain the open_id, the refresh token is considered invalid
        # This could happen if the token structure is incorrect or has been tampered with
        if not open_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Create a new access token for the user
        # This token will be used for authenticating subsequent requests
        new_access_token = await create_access_token(data={"sub": open_id})

        # Create a new refresh token for the user
        # This token will be used to obtain new access tokens when the current one expires
        new_refresh_token = await create_refresh_token(data={"sub": open_id})

        # Return both the new access token and refresh token to the frontend
        # The client should store these securely and use them for future requests
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }

    except HTTPException as he:
        # Log any HTTP exceptions that occur during the token refresh process
        # These are typically related to authentication issues (e.g., invalid or expired tokens)
        logger.warning(f"Token refresh failed with HTTP error: {str(he)}")
        # Re-raise the exception to be handled by the caller or middleware
        raise

    except Exception as e:
        # Log any unexpected exceptions that occur during the token refresh process
        # These could be due to database errors, network issues, or other system problems
        logger.error(f"Unexpected error during token refresh: {str(e)}")
        # Convert the unexpected exception to an HTTP 500 error
        # This prevents exposing sensitive error details to the client
        raise HTTPException(status_code=500, detail="Internal server error during token refresh")


# TODO: Implement token blacklist functionality
def is_token_blacklisted(token: str) -> bool:
    """
    Check if the given token is blacklisted.

    Args:
        token (str): The token to check

    Returns:
        bool: True if the token is blacklisted, False otherwise

    TODO: Implement this functionality, may require interaction with a database or cache system
    """
    # Temporarily return False, indicating the token is not blacklisted
    return False


# TODO: Implement functionality to add a token to the blacklist
def add_to_blacklist(token: str) -> None:
    """
    Add a token to the blacklist.

    Args:
        token (str): The token to be added to the blacklist

    TODO: Implement this functionality, may require interaction with a database or cache system
    """
    # Temporary pass, indicating this functionality is not yet implemented
    pass
