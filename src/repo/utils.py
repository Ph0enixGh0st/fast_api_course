from datetime import date

from sqlalchemy import select, func

from src.models.bookings_models import BookingsModel
from src.models.rooms_models import RoomsModel


def rooms_ids_for_booking(
        date_from: date,
        date_to: date,
        hotel_id: int | None = None,
):
    rooms_count = (
        select(BookingsModel.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsModel)
        .filter(
            BookingsModel.date_from <= date_to,
            BookingsModel.date_to >= date_from,
        )
        .group_by(BookingsModel.room_id)
        .cte(name="rooms_count")
    )

    rooms_available = (
        select(
            RoomsModel.id.label("room_id"),
            (RoomsModel.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
        )
        .select_from(RoomsModel)
        .outerjoin(rooms_count, RoomsModel.id == rooms_count.c.room_id)
        .cte(name="rooms_available")
    )

    rooms_ids_for_hotel = (
        select(RoomsModel.id)
        .select_from(RoomsModel)
    )
    if hotel_id is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)

    rooms_ids_for_hotel = (
        rooms_ids_for_hotel
        .subquery(name="rooms_ids_for_hotel")
    )

    rooms_ids_to_get = (
        select(rooms_available.c.room_id)
        .select_from(rooms_available)
        .filter(
            rooms_available.c.rooms_left > 0,
            rooms_available.c.room_id.in_(rooms_ids_for_hotel),
        )
    )
    return rooms_ids_to_get