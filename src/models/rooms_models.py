from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from src.database import BaseModel


class RoomsModel(BaseModel):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str]
    description: Mapped[str | None]
    price_per_night: Mapped[int]
    quantity: Mapped[int]
