"""
app/api/routers/v1/instruments.py

This module defines the API routes related to instrument operations for version 1 of the API.
It provides endpoints for submitting instrument usage records to be stored in a database.

Main Components:
- Router setup for instrument-related endpoints: Configures API routes for managing instrument data.
- Dependency injection for repository access: Leverages FastAPI's dependency injection for accessing
  the instrument record repository seamlessly.

Endpoint Details:
- POST /submit_sequencing_record: Allows clients to submit new instrument usage records. The records
  are validated using the InstrumentUsageRecordSchema and then saved in the repository.

Integrations:
- Operates in coordination with instrument schemas and CRUD operations defined in the application.
- Utilizes FastAPI dependencies for efficient integration with repository operations.

Usage Example:
The module's primary function is posting new instrument usage records, facilitated by the API's routing:

    @router.post("/submit_sequencing_record", response_model=MessageResponse)
    async def create_instrument_usage_record(
            new_instrument_record: InstrumentUsageRecordSchema,
            instrument_repo: Annotated[InstrumentRecordRepository, Depends(get_instrument_record_repository)]
    ) -> Dict[str, str]:
        ...

Dependencies:
- FastAPI: For establishing routes and managing dependency injection.
- Pydantic: Utilized for data validation and serialization of instrument usage records.
- Instrument CRUD repository: Handles operations related to instrument usage records within
  the database context.

This module is a crucial part of the FastAPI application, acting as a conduit for managing
instrument usage data and ensuring their correct storage and retrieval within the system.
"""

from fastapi import (
    APIRouter,
    HTTPException
)
from typing import (
    Annotated,
    Dict
)
from app.crud.WeChat.instrument import (
    InstrumentRecordRepository,
    get_instrument_record_repository
)
from app.schemas.WeChat.message import MessageResponse
from app.schemas.WeChat.instruments import InstrumentUsageRecord as InstrumentUsageRecordSchema
from fastapi import Depends

router = APIRouter()


@router.post("/submit_instrument_usage_record", response_model=MessageResponse)
async def create_instrument_usage_record(
        new_instrument_record: InstrumentUsageRecordSchema,
        instrument_repo: Annotated[InstrumentRecordRepository, Depends(get_instrument_record_repository)]
) -> Dict[str, str]:
    """
    Creates a new instrument usage record.

    This endpoint creates and submits a new sequencing record. It accepts record
    data and stores it in a repository.

    Args:
        new_instrument_record (InstrumentUsageRecordSchema): An object with details
            of the instrument usage record, validated and serialized according to
            InstrumentUsageRecordSchema.

        instrument_repo (InstrumentRecordRepository): A repository instance for
            managing and persisting instrument usage records, injected via FastAPI's
            dependency system.

    Returns:
        dict: A dictionary containing a success message upon successful creation
              of the record.

    Raises:
        HTTPException: If any exception occurs during the record creation, raises
            an HTTP 500 error with the exception message.
    """
    try:
        # Attempt to create a new record in the repository using the provided data
        await instrument_repo.create_record(new_instrument_record)

        # Return a success message if the record is created successfully
        return {"message": "New sequencing record successfully created"}
    except Exception as e:
        # If an error occurs, raise an HTTPException with status code 500 and the error details
        raise HTTPException(status_code=500, detail=str(e))
