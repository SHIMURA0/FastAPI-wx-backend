from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    JSON,
    ForeignKey
)
from sqlalchemy.sql import func
from app.db.base import Base


class RoomUsageRecord(Base):
    __tablename__ = "ROOM_USAGE_RECORDS"
    # Primary key
    id = Column(Integer, primary_key=True, index=True, comment="Record ID")

    # Core information
    room_id = Column(Integer, ForeignKey("ROOMS.id"), nullable=False, comment="Indexing ID for rooms")
    operator_id = Column(
        Integer,
        ForeignKey("USERS.id"),
        nullable=False,
        comment="Name of the operator performing the device"
    )
    room_status = Column(String(255), nullable=False, comment="parameter indicating whether entering or leaving a room")
    operator_type = Column(String(255), nullable=False, comment="daily or extraction")

    # Additional details stored as JSON
    details = Column(JSON, nullable=False, comment="detailed record of instruments used in the room")

    # Automatically managed timestamp fields
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="Timestamp of record creation")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="Timestamp of last record update")

# TODO: Add models for other types of instruments as needed.
