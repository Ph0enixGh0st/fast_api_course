from sqlalchemy import select, func

from src.models.amenities_models import AmenitiesModel, RoomAmenitiesModel
from src.schemas.amenities_schemas import AmenitiesPrintOut, PaginatedAmenitiesPrintOut, RoomAmenity
from src.schemas.pagination import PaginationParams
from src.repo.base import BaseRepository


class AmenitiesRepository(BaseRepository):
    model = AmenitiesModel
    schema = AmenitiesPrintOut

    async def get_all_amenities(self, pagination: PaginationParams):
        total_query = select(func.count()).select_from(AmenitiesModel)
        total = await self.session.scalar(total_query)

        offset = (pagination.page - 1) * pagination.per_page
        query = select(AmenitiesModel).order_by(AmenitiesModel.id).offset(offset).limit(pagination.per_page)
        result = await self.session.execute(query)
        amenities = result.scalars().all()

        return PaginatedAmenitiesPrintOut(
            page=pagination.page,
            per_page=pagination.per_page,
            total_found=total,
            amenities=amenities,
        )


class RoomAmenitiesRepository(BaseRepository):
    model = RoomAmenitiesModel
    schema = RoomAmenity
