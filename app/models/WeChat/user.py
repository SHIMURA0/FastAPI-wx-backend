# File: FastAPI-Wechat/app/models/user.py
# Description: Defines the database model for WeChat users
# Author: [Your Name]
# Created: [YYYY-MM-DD]
# Last Modified: [YYYY-MM-DD]

from sqlalchemy import (
    Column,
    Integer,
    String,
)
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

    id: int = Column(Integer, primary_key=True, index=True, comment="User ID, primary key")
    real_name: str = Column(String(255), nullable=True, comment="User's real name")
    openid: str = Column(String(255), unique=True, comment="WeChat user's OpenID, unique")
