<<<<<<< Updated upstream
from sqlalchemy import Column, Integer, String
from db.database import Base


class DbUser(Base):
    __tablename__: str = 'user'
    id: Column[int] = Column(Integer, primary_key=True, index=True, comment='cest quoi un comment sur une collone d`une table')
    username: Column[str] = Column(String(40))
    email: Column[str] = Column(String(70))
    hashed_password: Column[str] = Column(String)
=======
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base
from datetime import datetime


class DbUser(Base):
    __tablename__: str = "user"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        comment="Unique identifier for the user (Auto-incrementing PK).",
    )
    username: Mapped[str] = mapped_column(
        String(40),
        unique=True,
        nullable=False,
        comment="Unique display name. Used for public profile URLs and mentions.",
    )
    email: Mapped[str] = mapped_column(
        String(70),
        unique=True,
        nullable=False,
        comment="Primary contact email. Must be unique and verified for login.",
    )
    hashed_password: Mapped[str] = mapped_column(
        String,
        comment="Werkzeug hash (scrypt:32768:8:1). Use check_password_hash to verify.",
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Timestamp of when the account was created.",
    )
>>>>>>> Stashed changes
