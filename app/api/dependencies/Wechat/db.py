# app/api/dependencies/db.py

"""
This module provides FastAPI dependency functions for managing database sessions.

It includes the `get_db_dependency` function, which serves as a FastAPI
dependency injection point for obtaining an asynchronous SQLAlchemy session.

Usage:
    Use `get_db_dependency` in your FastAPI route handlers as follows:

    ```
    @app.get("/items/")
    async def read_items(db: AsyncSession = Depends(get_db_dependency)):
        ...
    ```
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_db


async def get_db_dependency(
        db: AsyncSession = Depends(get_async_db)
) -> AsyncSession:
    """Provide an asynchronous database session for FastAPI routes.

    This function retrieves an asynchronous SQLAlchemy session from the
    `get_async_db` dependency, making it available for use in route
    handlers.

    Args:
        db (AsyncSession): An instance of AsyncSession retrieved from
        the `get_async_db` dependency. This session can be used for
        performing database operations.

    Returns:
        AsyncSession: The database session that can be utilized in
        route functions for performing CRUD operations.
    """
    return db
