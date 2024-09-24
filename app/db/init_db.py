# app/db/init_db.py

import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine
)
from app.db.base import Base

# Load environment variables from .env file
# This allows us to keep sensitive information like database credentials out of the code
load_dotenv()

# Retrieve the database URL from environment variables
# The DATABASE_URL should be in the format: postgresql+asyncpg://user:password@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL")

# Check if DATABASE_URL is set, raise an error if it's not
# This ensures that we don't proceed without a valid database connection string
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL set for the application. Please check your .env file.")

# Create an asynchronous SQLAlchemy engine
# AsyncEngine is used for non-blocking database operations
# 'echo=True' enables SQL query logging for debugging purposes
# Consider setting this to False in production for better performance
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)


async def init_db() -> None:
    """
    Initialize the database by creating all tables defined in the SQLAlchemy models.

    This function creates a new database connection and uses it to create
    all tables that are associated with the declarative base (Base).
    It's typically called once when the application starts.

    Note: This will not update existing tables if your models change.
    For schema migrations, consider using tools like Alembic.
    """
    async with engine.begin() as conn:
        # Use run_sync to run the synchronous create_all method in an async context
        # This creates tables for all models that inherit from Base
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """
    Close the database connection pool.

    This function should be called when shutting down the application
    to ensure all database connections are properly closed.
    It helps prevent connection leaks and ensures clean application shutdown.
    """
    await engine.dispose()
