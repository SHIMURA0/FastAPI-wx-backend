# File: app/models/instruments.py
# Environment: conda env:your_environment_name (Python 3.x)
# Author: Your Name
# Date Created: YYYY-MM-DD
# Last Modified: YYYY-MM-DD

import uuid
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    JSON, ForeignKey
)
from sqlalchemy.future import select
from sqlalchemy.sql import func
from app.db.base import Base


class InstrumentUsageRecord(Base):
    """
    Represents a record of a sequencing operation in the database.

    This model captures essential details about a sequencing process, including
    the operator, instrument details, operation date, and additional information
    stored as JSON.

    Attributes:
        id (int): The primary key of the record.
        instrument (str): The name or identifier of the sequencing instrument used.
        instrument_status (str): The current status of the instrument during the operation.
        operator_name (str): The name of the person operating the sequencing instrument.
        operation_date (datetime): The date and time when the sequencing operation was performed.
        details (JSON): Additional details about the sequencing operation stored as a JSON object.
        created_at (datetime): The timestamp when the record was created (auto-set).
        updated_at (datetime): The timestamp when the record was last updated (auto-updated).
    """

    __tablename__ = "INSTRUMENT_USAGE_RECORDS"

    # Primary key
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    # Core information
    instrument_code = Column(String(255), ForeignKey("INSTRUMENTS.code"), nullable=False, comment="instrument code")
    instrument = Column(String(255), ForeignKey("INSTRUMENTS.name"), nullable=False,
                        comment="Name or identifier of the device")
    instrument_status = Column(String(255), nullable=False, comment="Status of the instrument during device operation")
    operator_name = Column(
        String(255),
        ForeignKey("USERS.real_name"),
        nullable=False,
        comment="Name of the operator performing the device"
    )

    # Additional details stored as JSON
    details = Column(JSON, nullable=False, comment="Additional device operation details in JSON format")

    # Automatically managed timestamp fields (UTC datatime)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="Timestamp of record creation")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="Timestamp of last record update")

    @staticmethod
    async def generate_id(session):
        # 创建查询
        stmt = select(func.max(InstrumentUsageRecord.id))  # 使用 record_id 替换 id

        # 执行查询
        result = await session.execute(stmt)

        # 获取最大 ID
        max_id = result.scalar()  # 获取标量值
        return (max_id + 1) if max_id is not None else 1

    def __repr__(self):
        """
        Provide a string representation of the SequencingRecord instance.

        Returns:
            str: A string representation of the SequencingRecord object.
        """
        return f"<SequencingRecord(id={self.id}, operator={self.operator_name}, instrument={self.instrument})>"

# TODO: Add models for other types of instruments as needed.
# Example:
# class PCRRecord(Base):
#     __tablename__ = "pcr_records"
#     ...
