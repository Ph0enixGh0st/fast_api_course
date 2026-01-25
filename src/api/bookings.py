from fastapi import APIRouter, Body, Path, Query, HTTPException
from datetime import date

from src.api.dependencies import PaginationSettings, DBSpawner, CurrentUserId
from src.repo.bookings_repo import PaginatedBookingsPrintOut
from src.schemas.bookings_schemas import Booking, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("", response_model=PaginatedBookingsPrintOut)
async def get_all_bookings(
        db: DBSpawner,
        pagination: PaginationSettings
):
    return await db.bookings.get_all_bookings(pagination)


@router.post("/bookings")
async def create_booking(
        db: DBSpawner,
        user_id: CurrentUserId,
        booking_data: Booking = Body(...),
):
        room = await db.rooms.get_one_or_none(id=booking_data.room_id)
        if not room:
            raise HTTPException(404, "Room not found")

        _booking_data = BookingAdd(
            room_id=booking_data.room_id,
            user_id=user_id,
            date_from=booking_data.date_from,
            date_to=booking_data.date_to,
            price_per_night=room.price
        )

        booking = await db.bookings.add(_booking_data)
        await db.commit()

        return {"status": "success", "created": booking}
