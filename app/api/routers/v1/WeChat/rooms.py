"""
app/api/routers/v1/rooms.py

This module defines the API routes related to room operations for version 1 of the API.
It includes functionality for creating room usage records and committing them to the database.

Main Components:
- Router setup for room-related endpoints: Configures the routes for room operations within the API.
- Dependency injection for repository access: Utilizes FastAPI's dependency injection to handle
  interactions with the room usage records repository.

Endpoint Details:
- POST /submit_room_record: Accepts room usage data and stores it in the repository using the
  provided RoomUsageRecordSchema. Returns a success message upon successful creation.

Integrations:
- Works with room schemas and CRUD operations to manage room usage records effectively.
- Incorporates FastAPI dependencies to ensure seamless repository interactions.

Usage Example:
The primary interaction involves posting new room usage records to the specified endpoint,
facilitated through the router and repository:

    @router.post("/submit_room_record")
    async def create_room_usage_record(
            new_room_record: RoomUsageRecordSchema,
            room_repo: Annotated[RoomRecordRepository, Depends(get_room_record_repository)]
    ) -> Dict[str, str]:
        ...

Dependencies:
- FastAPI: For setting up routes and handling dependency injection.
- Pydantic: For data validation and serialization.
- CRUD repository: For performing operations on room usage records within a database context.

This module is an integral part of the FastAPI application, serving as the entry point for
handling room-related data submissions and ensuring data integrity and persistence.
"""

from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)
from typing import (
    Dict,
    Annotated
)
from app.schemas.WeChat.room import RoomUsageRecord as RoomUsageRecordSchema
from app.crud.WeChat.room import (
    RoomRecordRepository,
    get_room_record_repository
)

router = APIRouter()


@router.post("/submit_room_record")
async def create_room_usage_record(
        new_room_record: RoomUsageRecordSchema,
        room_repo: Annotated[RoomRecordRepository, Depends(get_room_record_repository)]
) -> Dict[str, str]:
    """
    Creates a new room usage record.

    This endpoint processes the submission of a new room usage record. It accepts
    room usage details and commits them to a repository.

    Args:
        new_room_record (RoomUsageRecordSchema): An object containing the details
            of the room usage record, validated and serialized according to
            RoomUsageRecordSchema.

        room_repo (RoomRecordRepository): A repository instance for managing and
            storing room usage records, injected via FastAPI's dependency system.

    Returns:
        dict: A dictionary containing a success message upon successful creation
              of the room usage record.

    Raises:
        HTTPException: Raises a 500 error if any exception occurs during the record
            creation process, including the error details.
    """
    try:
        # Attempt to create a new record in the repository using the provided data
        await room_repo.create_record(new_room_record)

        # Return a success message if the record is created successfully
        return {"message": "New room usage record successfully created"}
    except Exception as e:
        # If an error occurs, raise an HTTPException with status code 500 and the error details
        raise HTTPException(status_code=500, detail=str(e))
