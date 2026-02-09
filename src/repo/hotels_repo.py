from datetime import date

from sqlalchemy import select, func

from src.models.bookings_models import BookingsModel
from src.repo.mappers.mappers import HotelsPrintOutMapper, HotelWithRoomsMapper, RoomMapper
from src.schemas.pagination import PaginationParams
from src.models.hotels_models import HotelsModel
from src.models.rooms_models import RoomsModel
from src.repo.base import BaseRepository
from src.schemas.hotels_schemas import PaginatedHotelsPrintOut
from src.schemas.rooms_schemas import Room
from src.repo.utils import rooms_ids_for_booking


class HotelsRepository(BaseRepository):
    """
       Repository for hotel data operations.

       ⚠️NOTE: When defining routes that use this repository, place specific paths
       (like '/search') BEFORE parametric paths (like '/{hotel_id}') to avoid routing conflicts.
    """
    model = HotelsModel
    mapper = HotelsPrintOutMapper

    async def get_all_hotels(self, pagination: PaginationParams):
        total_query = select(func.count()).select_from(HotelsModel)
        total = await self.session.scalar(total_query)

        offset = (pagination.page - 1) * pagination.per_page
        query = select(HotelsModel).order_by(HotelsModel.id).offset(offset).limit(pagination.per_page)
        result = await self.session.execute(query)
        hotels = result.scalars().all()

        return PaginatedHotelsPrintOut(
            page=pagination.page,
            per_page=pagination.per_page,
            total_found=total,
            hotels=hotels,
        )


    async def search_hotels(
            self,
            pagination: PaginationParams,
            location: str = None,
            name: str = None,
            date_from: date = None,
            date_to: date = None,
        ):
        query = select(HotelsModel)
        if name:
            query = query.where(HotelsModel.name.ilike(f"%{name}%"))
        if location:
            query = query.where(HotelsModel.location.ilike(f"%{location}%"))
        if date_from and date_to:
            rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
            hotels_ids_to_get = (
                select(RoomsModel.hotel_id)
                .select_from(RoomsModel)
                .filter(RoomsModel.id.in_(rooms_ids_to_get))
            )
            query = query.where(HotelsModel.id.in_(hotels_ids_to_get))

        count_query = select(func.count()).select_from(query.subquery())
        total = await self.session.scalar(count_query)

        query = query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)

        result = await self.session.execute(query)
        hotels = result.scalars().all()

        if not hotels:
            return {"message": "No hotels found with your search criteria"}

        if date_from and date_to:
            hotel_ids = [h.id for h in hotels]

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
            rooms_left = (
                RoomsModel.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)
            ).label("rooms_left")

            rooms_query = (
                select(RoomsModel, rooms_left)
                .outerjoin(rooms_count, RoomsModel.id == rooms_count.c.room_id)
                .filter(
                    RoomsModel.hotel_id.in_(hotel_ids),
                    rooms_left > 0,
                )
            )
            rooms_result = await self.session.execute(rooms_query)
            rooms_by_hotel: dict[int, list[Room]] = {}
            for room, rl in rooms_result.all():
                r = RoomMapper.map_to_domain_entity(room, rooms_left=rl)
                rooms_by_hotel.setdefault(room.hotel_id, []).append(r)

            hotels_out = [
                HotelWithRoomsMapper.map_to_domain_entity(h, rooms=rooms_by_hotel.get(h.id, []))
                for h in hotels
            ]
        else:
            hotels_out = hotels

        return PaginatedHotelsPrintOut(
            page=pagination.page,
            per_page=pagination.per_page,
            total_found=total,
            hotels=hotels_out,
        )


    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsModel.hotel_id)
            .select_from(RoomsModel)
            .filter(RoomsModel.id.in_(rooms_ids_to_get))
        )
        return await self.get_filtered(HotelsModel.id.in_(hotels_ids_to_get))