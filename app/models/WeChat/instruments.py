from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func
from app.db.base import Base


class Instruments(Base):
    __tablename__ = "INSTRUMENTS"

    # Primary key
    id: int = Column(Integer, primary_key=True, index=True, comment="Indexing ID for each device")

    # Core information
    code: str = Column(String(255), nullable=False, unique=True, comment="device code")
    name: str = Column(String(255), nullable=False, comment="device name")
    brand: str = Column(String(255), nullable=True, comment="device brand")
    specifications_and_model: str = Column(String(255), nullable=True, comment="device specifications and model")
    serial_number: str = Column(String(255), nullable=True, comment="device serial number")
    manufacturer: str = Column(String(255), nullable=True, comment="device manufacturer")
    room_id: str = Column(Integer, ForeignKey("ROOMS.id"), nullable=True, comment="device room id")
    usage_type: str = Column(String(255), nullable=True, comment="device usage type")
    remark: str = Column(String(255), nullable=True, comment="device remark")

    # Automatically managed timestamp fields
    created_at: DateTime = Column(DateTime(timezone=True), server_default=func.now(),
                                  comment="Timestamp of record creation")
    updated_at: DateTime = Column(DateTime(timezone=True), onupdate=func.now(),
                                  comment="Timestamp of last record update")
