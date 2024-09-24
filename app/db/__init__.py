# app/db/__init__.py

from .base import Base
from .init_db import (
    engine,
    init_db,
    close_db
)
from .session import (
    get_async_db,
)

__all__ = [
    "Base",  # SQLAlchemy declarative base class for defining ORM models
    "engine",  # SQLAlchemy asynchronous database engine
    "init_db",  # Asynchronous function to initialize the database
    "close_db",  # Asynchronous function to close database connections
    "get_async_db",  # Generator function to create asynchronous database sessions
]

# This __init__.py file serves as the main entry point for the database module.
# It imports and exposes key components for database operations:

# 1. Base: The declarative base class from SQLAlchemy, used as a foundation
#    for all ORM model definitions in the application.

# 2. engine: The asynchronous SQLAlchemy engine, configured to connect to
#    the database specified in the application's settings.

# 3. init_db: An asynchronous function that initializes the database,
#    typically called during application startup to ensure schema is in place.

# 4. close_db: An asynchronous function to properly close database connections,
#    usually called during application shutdown for clean resource management.

# 5. get_async_db: A dependency function that yields asynchronous database
#    sessions, designed for use with FastAPI's dependency injection system.

# By centralizing these imports and using __all__, we provide a clean,
# controlled interface for other parts of the application to interact
# with the database layer, promoting better organization and encapsulation.
