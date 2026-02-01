from datetime import date
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PostgreSQL_UUID
import uuid

from src.database import BaseModel


class BookingsModel(BaseModel):
    __tablename__ = "bookings"

    id: Mapped[UUID] = mapped_column(
        PostgreSQL_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price_per_night: Mapped[int]

    @hybrid_property
    def total_nights(self) -> int:
        return (self.date_to - self.date_from).days

    @hybrid_property
    def total_cost(self) -> int:
        return self.price_per_night * self.total_nights
