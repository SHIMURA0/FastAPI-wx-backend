# File: FastAPI-Wechat/app/models/user.py
# Description: Defines the database model for WeChat users
# Author: [Your Name]
# Created: [YYYY-MM-DD]
# Last Modified: [YYYY-MM-DD]

from sqlalchemy import (
    Column,
    Integer,
    String
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func
from app.db.base import Base


class User(Base):
    """
    User model class

    This class defines the database model for storing basic information about WeChat users.

    Attributes:
        __tablename__ (str): Name of the database table
        id (Column): Unique identifier for the user, primary key
        real_name (Column): Real name of the user
        openid (Column): WeChat OpenID of the user, unique index
    """

    __tablename__ = "USERS"

    id: int = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="User ID, primary key"
    )
    real_name: str = Column(
        String(255),
        nullable=True,
        unique=False,
        comment="User's real name"
    )
    openid: str = Column(
        String(255),
        unique=True,
        comment="WeChat user's OpenID, unique"
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
        stmt = select(func.max(User.id))

        # execute the query
        result = await session.execute(stmt)

        # get the maximum id in the table INSTRUMENT_USAGE_RECORDS up to now
        max_id: int = result.scalar()
        return (max_id + 1) if max_id is not None else 1
