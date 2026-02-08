from sqlalchemy import select, func, delete, insert

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

    async def set_room_amenities(self, room_id: int, amenity_ids: list[int]) -> None:
        get_current_amenities_ids_query = (
            select(self.model.amenity_id)
            .filter_by(room_id=room_id)
        )
        res = await self.session.execute(get_current_amenities_ids_query)
        current_amenities_ids: list[int] = res.scalars().all()
        ids_to_delete: list[int] = list(set(current_amenities_ids) - set(amenity_ids))
        ids_to_insert: list[int] = list(set(amenity_ids) - set(current_amenities_ids))

        if ids_to_delete:
            delete_m2m_amenities_stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.amenity_id.in_(ids_to_delete),
                )
            )
            await self.session.execute(delete_m2m_amenities_stmt)

        if ids_to_insert:
            insert_m2m_amenities_stmt = (
                insert(self.model)
                .values([{"room_id": room_id, "amenity_id": f_id} for f_id in ids_to_insert])
            )
            await self.session.execute(insert_m2m_amenities_stmt)