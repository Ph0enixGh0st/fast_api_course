from sqlalchemy import select, func

from src.models.rooms_models import RoomsModel
from src.repo.base import BaseRepository
from src.schemas.rooms_schemas import Room


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = Room

    async def search_rooms(
            self,
            hotel_id,
            name,
            description
        ):
        query = select(RoomsModel).where(RoomsModel.hotel_id==hotel_id)
        if name:
            query = query.where(RoomsModel.name.ilike(f"%{name}%"))
        if description:
            query = query.where(RoomsModel.description.ilike(f"%{description}%"))

        result = await self.session.execute(query)
        rooms = result.scalars().all()

        if not rooms:
            return {"message": "No rooms found with your search criteria"}

        return rooms