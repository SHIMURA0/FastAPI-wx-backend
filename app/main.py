"""
FastAPI Application for WeChat Integration.

This module initializes a FastAPI application with database connection management
and API routing for WeChat-related endpoints. It includes a lifespan context manager
for database connection setup and teardown.

Modules:
    - fastapi: The FastAPI framework for building APIs.
    - contextlib: For creating context managers.
    - app.api: Contains API routers for WeChat functionality.
    - app.db: Contains functions for initializing and closing the database connection.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import api_router
from app.db import (
    init_db,
    close_db
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Manage the lifespan of the FastAPI application.

    This function initializes the database connection at startup and
    closes it at shutdown.

    Args:
        _app (FastAPI): The FastAPI application instance.
    """
    await init_db()  # Initialize the database
    yield  # Control returns here for handling requests
    await close_db()  # Close the database connection


app = FastAPI(lifespan=lifespan)

# Include the API router for WeChat endpoints with a specified prefix.
app.include_router(api_router, prefix="/api/v1/wechat")


@app.get("/")
async def root():
    """Root endpoint for the FastAPI application.

    Returns:
        dict: A JSON response containing a welcome message.
    """
    return {"message": "Welcome!"}


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application on the specified host and port.
    uvicorn.run(app, host="0.0.0.0", port=8000)
