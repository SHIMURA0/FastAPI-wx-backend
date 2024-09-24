# app/crud/room.py

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends
from app.schemas.WeChat.room import RoomUsageRecord as RoomUsageRecordSchema
from app.models.WeChat.room_usage_records import RoomUsageRecord as RoomUsageRecordModel
from app.api.dependencies.Wechat.db import get_db_dependency
from app.db.session import get_async_db


class RoomRecordRepository:
    def __init__(
            self,
            db: AsyncSession
    ) -> None:
        self.db: AsyncSession = db

    async def create_record(
            self,
            room_record: RoomUsageRecordSchema
    ) -> RoomUsageRecordModel:
        # Convert Pydantic model to ORM model
        db_record = RoomUsageRecordModel(**room_record.model_dump())

        # Add the new record to the database session
        self.db.add(db_record)

        # Commit the transaction to persist the record
        await self.db.commit()

        # Refresh the record to ensure it reflects the current database state,
        # including any auto-generated fields like the ID
        await self.db.refresh(db_record)

        # Return the newly created record
        return db_record


async def get_room_record_repository(
        db: Annotated[AsyncSession, Depends(get_async_db)]
) -> RoomRecordRepository:
    return RoomRecordRepository(db)
