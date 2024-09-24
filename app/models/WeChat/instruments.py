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
    id = Column(Integer, primary_key=True, index=True, comment="Indexing ID for each device")

    # Core information
    code = Column(String(255), nullable=False, unique=True, comment="device code")
    name = Column(String(255), nullable=False, unique=True, comment="device name")
    brand = Column(String(255), nullable=False, unique=True, comment="device brand")
    specifications_and_model = Column(String(255), nullable=False, comment="device specifications and model")
    serial_number = Column(String(255), nullable=False, unique=True, comment="device serial number")
    manufacturer = Column(String(255), nullable=False, comment="device manufacturer")
    room_id = Column(Integer, ForeignKey("ROOMS.id"), nullable=False, unique=True, comment="device room id")
    usage_type = Column(String(255), nullable=True, comment="device usage type")
    remark = Column(String(255), nullable=True, comment="device remark")

    # Automatically managed timestamp fields
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="Timestamp of record creation")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="Timestamp of last record update")
