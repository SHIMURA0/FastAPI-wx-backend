# app/core/config.py

"""
config.py: Application Configuration

This module defines the configuration settings for the FastAPI-WeChat application.
It uses environment variables and the python-dotenv library to manage configuration,
ensuring security and flexibility across different deployment environments.

The Settings class encapsulates all configuration parameters, including:
- JWT (JSON Web Token) settings
- WeChat Mini Program credentials
- OAuth2 authentication scheme
- General project settings

Usage:
    from app.core.config import settings

    # Access configuration variables
    secret_key = settings.JWT_SECRET_KEY
    app_name = settings.PROJECT_NAME

Note:
    Make sure to set up a .env file in the project root with the necessary
    environment variables, or set them in your deployment environment.
"""

import os
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()


class Settings:
    """
    Settings class to store all configuration variables.

    This class uses environment variables to configure the application.
    It's designed to be instantiated once and used throughout the application.
    """

    # JWT settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # WeChat Mini Program settings
    WECHAT_APP_ID: str = os.getenv("WECHAT_APP_ID")
    WECHAT_APP_SECRET: str = os.getenv("WECHAT_APP_SECRET")

    # OAuth2 scheme for token authentication
    OAUTH2_SCHEME: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

    # General project settings
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")

    class Config:
        """
        Inner Config class to specify additional settings for pydantic.

        This tells pydantic to read the .env file for any unset environment variables.
        """
        env_file = ".env"


# Instantiate the Settings class
# This creates a single instance of Settings to be used throughout the application
settings = Settings()
