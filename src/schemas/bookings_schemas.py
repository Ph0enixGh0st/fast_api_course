from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Booking(BaseModel):
    """Represents a basic booking with name and location."""
    room_id: int
    date_from: date
    date_to: date

class BookingAdd(Booking):
    price_per_night: int
    user_id: int


class BookingsPrintOut(BaseModel):
    """Represents the full output structure of a booking, including ID."""
    id: UUID
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price_per_night: int

    model_config = ConfigDict(from_attributes=True)

