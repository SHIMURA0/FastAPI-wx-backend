# app/crud/room.py

"""
This module provides the RoomRecordRepository class for managing room usage
records in the database using SQLAlchemy. It includes methods for creating
new records and handling database interactions.

The repository uses asynchronous database sessions and is designed to be
used with FastAPI. It handles various exceptions related to database
operations and validates input using Pydantic models.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends
from app.schemas.WeChat.room import RoomUsageRecord as RoomUsageRecordSchema
from app.models.WeChat.room_usage_records import RoomUsageRecord as RoomUsageRecordModel
from sqlalchemy.exc import (
    SQLAlchemyError,
    IntegrityError
)
from pydantic import ValidationError
import logging
from app.api.dependencies.Wechat.db import get_db_dependency

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RoomRecordRepository:
    """Repository for managing room usage records in the database."""

    def __init__(self, db: AsyncSession) -> None:
        """
        Initialize the RoomRecordRepository with a database session.

        Args:
            db (AsyncSession): The database session to be used for operations.
        """
        self.db: AsyncSession = db

    async def create_record(
            self,
            room_record: RoomUsageRecordSchema
    ) -> RoomUsageRecordModel:
        """
        Create a new room usage record in the database.

        This method converts a Pydantic model to an ORM model, adds it to the
        database session, and commits the transaction.

        Args:
            room_record (RoomUsageRecordSchema): The room usage record data
            to be added to the database.

        Returns:
            RoomUsageRecordModel: The created room usage record model instance.

        Raises:
            IntegrityError: If there is a database integrity error while
            creating the record.
            ValidationError: If the input data is invalid.
            SQLAlchemyError: If there is a database error during the operation.
            Exception: For any unexpected errors that occur during the process.
        """
        try:
            # Convert Pydantic model to ORM model
            new_id: int = await RoomUsageRecordModel.generate_id(self.db)
            details_json_string: str = await RoomUsageRecordModel.convert_details_to_json_string(room_record.details)
            db_record: RoomUsageRecordModel = RoomUsageRecordModel(
                id=new_id,
                room_id=room_record.room_id,
                operator_name=room_record.operator_name,
                room_status=room_record.room_status,
                operation_type=room_record.operation_type,
                details=details_json_string
            )
            # Add the new record to the database session
            self.db.add(db_record)

            # Commit the transaction to persist the record
            await self.db.commit()

            # Refresh the record to ensure it reflects the current database state,
            # including any auto-generated fields like the ID
            await self.db.refresh(db_record)

            # Return the newly created record
            return db_record

        except IntegrityError as e:
            logger.error("Integrity error while creating record with data %s: %s", room_record, e)
            await self.db.rollback()
            raise

        except ValidationError as ve:
            logger.error("Validation error with data %s: %s", room_record, ve)
            raise

        except SQLAlchemyError as e:
            logger.error("Database error during record creation with data %s: %s", room_record, e)
            await self.db.rollback()
            raise

        except Exception as e:
            logger.error("Unexpected error while creating record with data %s: %s", room_record, e)
            raise


async def get_room_record_repository(
        db: Annotated[AsyncSession, Depends(get_db_dependency)]
) -> RoomRecordRepository:
    """Dependency function to get the RoomRecordRepository instance.

    Args:
        db (AsyncSession): The database session dependency.

    Returns:
        RoomRecordRepository: An instance of RoomRecordRepository.
    """
    return RoomRecordRepository(db)
