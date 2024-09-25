# app/db/session.py

"""
This module provides an asynchronous database session management utility
using SQLAlchemy for FastAPI applications.

It creates an asynchronous session factory and defines a function to provide
database sessions as dependencies within FastAPI route functions.

The `get_async_db` function yields an SQLAlchemy `AsyncSession` for use
in database operations, automatically managing the lifecycle of the
database session.
"""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker
)
from typing import AsyncGenerator
from .init_db import engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create an asynchronous session factory.
# This factory creates new AsyncSession objects when called.
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,  # Bind the session to our async engine defined in init_db.py
    class_=AsyncSession,  # Specify that we want AsyncSession instances
    expire_on_commit=False,  # Prevent SQLAlchemy from expiring objects after commit
    # This is useful for avoiding unexpected behavior when accessing objects after a session is closed
)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Asynchronous database session dependency.

    This function is a dependency that can be used in FastAPI route functions.
    It creates and yields an AsyncSession, which can be used for database operations.
    The session is automatically closed when the request is completed.

    Yields:
        AsyncSession: An asynchronous SQLAlchemy session.

    Raises:
        Exception: If an error occurs during database operations.

    Example usage in a FastAPI route:
        @app.get("/items")
        async def read_items(db: AsyncSession = Depends(get_async_db)):
            # Use db for database operations
            items = await db.execute(select(Item))
            return items.scalars().all()

    Notes:
        This function uses a context manager to ensure proper session management.
        The yielded session is closed in the 'finally' block, ensuring cleanup
        even if an exception occurs.
        This pattern allows for efficient connection pooling and proper resource management.
    """
    async with AsyncSessionLocal() as session:
        logger.info("Database session opened")
        try:
            yield session
        except Exception as e:
            logger.error("Error during database session: %s", e)
            raise
        finally:
            logger.info("Database session closed")
            await session.close()

# Additional notes:
# - AsyncSessionLocal is a factory, not a class. It creates new session objects when called.
# - The async_sessionmaker is configured with expire_on_commit=False to prevent unexpected behavior
#   when accessing objects after the session is closed.
# - The get_async_db function is designed to be used with FastAPI's dependency injection system.
# - By using async/await, we ensure non-blocking database operations, which is crucial for
#   maintaining high concurrency in FastAPI applications.
