from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BigInteger, Date
from typing import Optional
from datetime import date

from src.database import BaseModel


class UsersModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100))

    # Optional fields
    first_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    dob: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    nick_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    avatar: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)