from src.models.rooms_models import RoomsModel
from src.repo.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsModel
