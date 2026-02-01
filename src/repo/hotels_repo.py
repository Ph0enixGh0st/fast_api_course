from datetime import date

from sqlalchemy import select, func

from src.schemas.pagination import PaginationParams
from src.database import engine
from src.models.hotels_models import HotelsModel
from src.models.rooms_models import RoomsModel
from src.repo.base import BaseRepository
from src.schemas.hotels_schemas import HotelsPrintOut, PaginatedHotelsPrintOut
from src.repo.utils import rooms_ids_for_booking


class HotelsRepository(BaseRepository):
    """
       Repository for hotel data operations.

       ⚠️NOTE: When defining routes that use this repository, place specific paths
       (like '/search') BEFORE parametric paths (like '/{hotel_id}') to avoid routing conflicts.
    """
    model = HotelsModel
    schema = HotelsPrintOut

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
            location,
            name
        ):
        # Build base query with optional filters
        query = select(HotelsModel)
        if name:
            query = query.where(HotelsModel.name.ilike(f"%{name}%"))
        if location:
            query = query.where(HotelsModel.location.ilike(f"%{location}%"))

        # Count total results
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.session.scalar(count_query)

        # Apply pagination
        query = query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)

        print(query.compile(engine, compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)
        hotels = result.scalars().all()

        if not hotels:
            return {"message": "No hotels found with your search criteria"}

        return PaginatedHotelsPrintOut(
            page=pagination.page,
            per_page=pagination.per_page,
            total_found=total,
            hotels=hotels,
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