from typing import TypedDict
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from .db_connection import Base
from datetime import datetime


class UserDict(TypedDict):
    id: int
    email: str
    first_name: str
    last_name: str
    role: str


class User(Base):  # ✅
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


class Skill(Base):  # ✅
    """
    Represents a skill that a user can have.

    Attributes:
        id (int): The unique identifier for the skill.
        name (str): The name of the skill.
    """

    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class UserSkill(Base):
    """
    Represents the relationship between a user and a skill.

    Attributes:
        user_id (int): The unique identifier for the user.
        skill_id (int): The unique identifier for the skill.
    """

    __tablename__ = 'users_skills'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    skill_id = Column(Integer, ForeignKey(
        'skills.id', ondelete='CASCADE'), primary_key=True)


class Work(Base):
    """
    Represents a work that a user has or had.

    Attributes:
        id (int): The unique identifier for the work.
        user_id (int): The unique identifier for the user.
        name (str): The name of the work.
        salary (float): The salary of the work.
        start_date (datetime): The start date of the work.
        end_date (datetime): The end date of the work (if any).
    """

    __tablename__ = 'works'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    salary = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime, nullable=True)


class UserCareer(Base):
    """
    Represents the relationship between a user and a career.

    Attributes:
        user_id (int): The unique identifier for the user.
        career_id (int): The unique identifier for the career.
        status (str): The status of the user in the career (cursando, graduado, expulsado, dimitido).
    """

    __tablename__ = 'users_careers'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    career_id = Column(Integer, ForeignKey('careers.id'), primary_key=True)
    status = Column(String)


class Career(Base):  # ✅
    """
    Represents a career that a user can take.

    Attributes:
        id (int): The unique identifier for the career.
        name (str): The name of the career.
        description (str): The description of the career.
        semesters (int): The number of semesters of the career.
        credits (int): The number of credits of the career.
        faculty_id (int): The unique identifier for the faculty.
    """

    __tablename__ = 'careers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    semesters = Column(Integer)
    credits = Column(Integer)
    faculty_id = Column(Integer, ForeignKey('faculties.id'))


class Faculty(Base):  # ✅
    """
    Represents a faculty that a career can belong to.

    Attributes:
        id (int): The unique identifier for the faculty.
        name (str): The name of the faculty.
    """

    __tablename__ = 'faculties'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
