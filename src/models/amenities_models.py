from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import BaseModel


class AmenitiesModel(BaseModel):
    __tablename__ = "amenities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500))

    rooms: Mapped[list["RoomsModel"]] = relationship(
        back_populates="amenities",
        secondary="room_amenities"
    )


class RoomAmenitiesModel(BaseModel):
    __tablename__ = "room_amenities"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    amenity_id: Mapped[int] = mapped_column(ForeignKey("amenities.id"))