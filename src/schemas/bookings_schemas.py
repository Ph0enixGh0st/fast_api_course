from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Booking(BaseModel):
    room_id: int
    date_from: date
    date_to: date

class BookingAdd(Booking):
    price_per_night: int
    user_id: int

class BookingTest(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price_per_night: int

class BookingsPrintOut(BaseModel):
    id: UUID
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price_per_night: int

    model_config = ConfigDict(from_attributes=True)
