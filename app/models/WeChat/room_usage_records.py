from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    JSON,
    ForeignKey,
    Index
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func
from app.db.base import Base


class RoomUsageRecord(Base):
    """Represents a record of room usage in the database.

    This model captures essential details about room usage, including the
    operator, room status, and additional information stored as JSON.

    Attributes:
        id (int): The primary key of the record.
        room_id (int): The ID of the room where the operation was performed.
        operator_name (str): The name of the operator performing the operation.
        room_status (str): The status indicating whether the operator is entering or leaving the room.
        operator_type (str): The type of operation performed (e.g., daily, extraction, CNAS).
        details (dict): Additional details about the instruments used in the room, stored as a JSON object.
        created_at (datetime): The timestamp when the record was created (auto-set).
        updated_at (datetime): The timestamp when the record was last updated (auto-updated).
    """

    __tablename__ = "ROOM_USAGE_RECORDS"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Record id for room usage"
    )

    # Core information
    room_id = Column(
        Integer,
        ForeignKey("ROOMS.id"),
        nullable=False,
        index=True,
        comment="Indicating the room id where operation is done"
    )
    operator_name = Column(
        String(255),
        ForeignKey("USERS.real_name"),
        nullable=False,
        index=True,
        comment="Name of the operator"
    )
    room_status = Column(
        String(255),
        nullable=False,
        comment="Indicating whether entering or leaving a room"
    )
    operator_type = Column(
        String(255),
        nullable=False,
        index=True,
        comment="daily or extraction or CNAS"
    )

    # Additional details stored as JSON
    details = Column(
        JSON,
        nullable=False,
        comment="Detailed record of instruments used in the room"
    )

    # Automatically managed timestamp fields
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Timestamp of record creation"
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Timestamp of last record update"
    )

    @staticmethod
    async def generate_id(
            session: AsyncSession
    ) -> int:
        """Generate a new unique ID for RoomUsageRecord.

        This method builds a SQL query to select the maximum ID from the
        ROOM_USAGE_RECORDS table and returns the next available ID.

        Args:
            session (AsyncSession): The database session to use for the query.

        Returns:
            int: The next available unique ID for RoomUsageRecord.
        """
        # build a SQL query
        stmt = select(func.max(RoomUsageRecord.id))

        # execute the query
        result = await session.execute(stmt)

        # get the maximum id in the table INSTRUMENT_USAGE_RECORDS up to now
        max_id = result.scalar()
        return (max_id + 1) if max_id is not None else 1

    def __repr__(self):
        return (f"<RoomUsageRecord(id={self.id},"
                f" room_id={self.room_id},"
                f" operator={self.operator_name})>")

# TODO: Add models for other types of instruments as needed.
