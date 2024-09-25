from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)
from sqlalchemy.sql import func
from app.db.base import Base


class Room(Base):
    __tablename__ = 'ROOMS'

    # Primary key
    id: int = Column(Integer, primary_key=True, index=True, comment="Indexing ID for each room")

    # Core information
    room_info: str = Column(String(255), comment="name and functionality of each room")

    # Automatically managed timestamp fields
    created_at: DateTime = Column(DateTime(timezone=True), server_default=func.now(),
                                  comment="Timestamp of record creation")
    updated_at: DateTime = Column(DateTime(timezone=True), onupdate=func.now(),
                                  comment="Timestamp of last record update")
