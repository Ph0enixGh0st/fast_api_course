from datetime import date

from src.schemas.bookings_schemas import BookingTest


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    # CREATE
    booking_data = BookingTest(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=2, day=15),
        date_to=date(year=2026, month=3, day=25),
        price_per_night=200,
    )
    new_booking_id = await db.bookings.add(booking_data)
    await db.commit()
    assert new_booking_id is not None

    # READ
    booking = await db.bookings.get_one_or_none(id=new_booking_id)
    assert booking is not None
    assert booking.room_id == room_id
    assert booking.user_id == user_id
    assert booking.date_from == date(2026, 2, 15)
    assert booking.date_to == date(2026, 3, 25)
    assert booking.price_per_night == 200

    # UPDATE (full)
    updated_data = BookingTest(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=4, day=1),
        date_to=date(year=2026, month=4, day=10),
        price_per_night=300,
    )
    updated_id = await db.bookings.update(new_booking_id, updated_data)
    await db.commit()
    assert updated_id is not None

    updated_booking = await db.bookings.get_one_or_none(id=new_booking_id)
    assert updated_booking.price_per_night == 300
    assert updated_booking.date_from == date(2026, 4, 1)
    assert updated_booking.date_to == date(2026, 4, 10)

    # EDIT (partial)
    from src.schemas.bookings_schemas import Booking
    partial_data = Booking(
        room_id=room_id,
        date_from=date(year=2026, month=5, day=1),
        date_to=date(year=2026, month=5, day=5),
    )
    edited_id = await db.bookings.edit(new_booking_id, partial_data)
    await db.commit()
    assert edited_id is not None

    edited_booking = await db.bookings.get_one_or_none(id=new_booking_id)
    assert edited_booking.date_from == date(2026, 5, 1)
    assert edited_booking.date_to == date(2026, 5, 5)
    assert edited_booking.price_per_night == 300

    # DELETE
    deleted_id = await db.bookings.delete(new_booking_id)
    await db.commit()
    assert deleted_id is not None

    deleted_booking = await db.bookings.get_one_or_none(id=new_booking_id)
    assert deleted_booking is None