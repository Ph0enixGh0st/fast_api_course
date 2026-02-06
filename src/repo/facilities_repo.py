from sqlalchemy import select, func

from src.models.facilities_models import FacilitiesModel, RoomFacilitiesModel
from src.schemas.facilities_schemas import FacilitiesPrintOut, PaginatedFacilitiesPrintOut, RoomFacility
from src.schemas.pagination import PaginationParams
from src.repo.base import BaseRepository


class FacilitiesRepository(BaseRepository):
    model = FacilitiesModel
    schema = FacilitiesPrintOut

    async def get_all_facilities(self, pagination: PaginationParams):
        total_query = select(func.count()).select_from(FacilitiesModel)
        total = await self.session.scalar(total_query)

        offset = (pagination.page - 1) * pagination.per_page
        query = select(FacilitiesModel).order_by(FacilitiesModel.id).offset(offset).limit(pagination.per_page)
        result = await self.session.execute(query)
        facilities = result.scalars().all()

        return PaginatedFacilitiesPrintOut(
            page=pagination.page,
            per_page=pagination.per_page,
            total_found=total,
            facilities=facilities,
        )


class RoomFacilitiesRepository(BaseRepository):
    model = RoomFacilitiesModel
    schema = RoomFacility
