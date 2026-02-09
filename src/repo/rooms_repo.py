from datetime import date

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, joinedload

from src.models.bookings_models import BookingsModel
from src.models.rooms_models import RoomsModel
from src.repo.base import BaseRepository
from src.repo.mappers.mappers import RoomMapper, RoomWithRelationsMapper
from src.schemas.rooms_schemas import Room
from src.repo.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = Room
    mapper = RoomMapper

    async def search_rooms(
            self,
            hotel_id: int,
            date_to: date,
            date_from: date,
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

        query = (
            select(RoomsModel, rooms_available.c.rooms_left)
            .join(rooms_available, RoomsModel.id == rooms_available.c.room_id)
            .options(
                selectinload(RoomsModel.facilities),
                selectinload(RoomsModel.amenities),
            )
            .filter(
                rooms_available.c.rooms_left > 0,
                RoomsModel.hotel_id == hotel_id,
            )
        )

        result = await self.session.execute(query)
        return [
            RoomWithRelationsMapper.map_to_domain_entity(room, rooms_left=rooms_left)
            for room, rooms_left in result.all()
        ]


    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(RoomsModel)
            .options(
                selectinload(RoomsModel.facilities),
                selectinload(RoomsModel.amenities),
            )
            .filter(RoomsModel.id.in_(rooms_ids_to_get))
        )

        result = await self.session.execute(query)
        return result.scalars().all()


    async def get_with_relations(self, **filter_by):
        query = (
            select(RoomsModel)
            .options(
                selectinload(RoomsModel.facilities),
                selectinload(RoomsModel.amenities),
                joinedload(RoomsModel.hotel),
            )
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return result.scalars().one_or_none()