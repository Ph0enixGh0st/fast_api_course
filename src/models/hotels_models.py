from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BigInteger

from src.database import BaseModel


class HotelsModel(BaseModel):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]
