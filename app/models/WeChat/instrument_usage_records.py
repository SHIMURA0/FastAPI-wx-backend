# File: app/models/instruments.py
# Environment: conda env:your_environment_name (Python 3.x)
# Author: Your Name
# Date Created: YYYY-MM-DD
# Last Modified: YYYY-MM-DD


from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    JSON, ForeignKey
)
from sqlalchemy.ext.asyncio import AsyncSession
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
        instrument_code (str): The code of the sequencing instrument used.
        instrument (str): The name or identifier of the sequencing instrument used.
        instrument_status (str): The current status of the instrument during the operation.
        operator_name (str): The name of the person operating the sequencing instrument.
        details (dict): Additional details about the sequencing operation stored as a JSON object.
        created_at (datetime): The timestamp when the record was created (auto-set).
        updated_at (datetime): The timestamp when the record was last updated (auto-updated).
    """

    __tablename__ = "INSTRUMENT_USAGE_RECORDS"

    # Primary key
    id: int = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    # Core information
    instrument_code: str = Column(
        String(255),
        nullable=False,
        comment="instrument code"
    )
    instrument: str = Column(
        String(255),
        nullable=False,
        comment="Name or identifier of the device"
    )
    instrument_status: str = Column(
        String(255),
        nullable=False,
        comment="Status of the instrument during device operation"
    )
    operator_name: str = Column(
        String(255),
        nullable=False,
        comment="Name of the operator performing the device"
    )

    # Additional details stored as JSON
    details: dict = Column(
        JSON,
        nullable=False,
        comment="Additional device operation details in JSON format"
    )

    # Automatically managed timestamp fields (UTC datatime)
    created_at: DateTime = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Timestamp of record creation"
    )
    updated_at: DateTime = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Timestamp of last record update"
    )

    @staticmethod
    async def generate_id(
            session: AsyncSession
    ) -> int:
        """Generate a new unique ID for InstrumentUsageRecord.

        This method builds a SQL query to select the maximum ID from the
        INSTRUMENT_USAGE_RECORDS table and returns the next available ID.

        Args:
            session (AsyncSession): The database session to use for the query.

        Returns:
            int: The next available unique ID for InstrumentUsageRecord.
        """
        # build a SQL query
        stmt = select(func.max(InstrumentUsageRecord.id))

        # execute the query
        result = await session.execute(stmt)

        # get the maximum id in the table INSTRUMENT_USAGE_RECORDS up to now
        max_id: int = result.scalar()
        return (max_id + 1) if max_id is not None else 1

    def __repr__(self) -> str:
        """Provide a string representation of the InstrumentUsageRecord instance.

        Returns:
            str: A string representation of the InstrumentUsageRecord object.
        """
        return (f"<InstrumentUsageRecord(id={self.id}, "
                f"operator={self.operator_name}, "
                f"instrument={self.instrument}, "
                f"status={self.instrument_status})>")

# TODO: Add models for other types of instruments as needed.
# Example:
# class PCRRecord(Base):
#     __tablename__ = "pcr_records"
#     ...
