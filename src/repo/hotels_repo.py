from sqlalchemy import select, func

from src.api.dependencies import PaginationSettings
from src.database import engine
from src.models.hotels_models import HotelsModel
from src.repo.base import BaseRepository
from src.schemas.hotels_schemas import PaginatedHotelsPrintOut


class HotelsRepository(BaseRepository):
    model = HotelsModel

    async def get_all_hotels(self, pagination: PaginationSettings):
        total_query = select(func.count()).select_from(HotelsModel)
        total = await self.session.scalar(total_query)

        offset = (pagination.page - 1) * pagination.per_page
        query = select(HotelsModel).offset(offset).limit(pagination.per_page)
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
            pagination: PaginationSettings,
            id,
            location,
            name
        ):
        # ID search (no pagination override)
        if id is not None:
            result = await self.session.execute(
                select(HotelsModel).where(HotelsModel.id == id)
            )
            hotel = result.scalar_one_or_none()
            if not hotel:
                return {"message": "No hotel found with given ID"}

            return PaginatedHotelsPrintOut(
                page=1,
                per_page=1,
                total_found=1,
                hotels=[hotel],
            )

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
