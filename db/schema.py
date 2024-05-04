from typing import TypedDict
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from .db_connection import Base
from datetime import datetime


class UserDict(TypedDict):
    id: int
    email: str
    first_name: str
    last_name: str
    role: str


class User(Base):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        role (str): The role of the user.
        is_active (bool): Indicates if the user is active or not.
        created_at (datetime): The date and time when the user was created.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String, default='user')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

    def to_UserDict(self) -> UserDict:
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role,
        }
