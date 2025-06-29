from src.models.users_models import UsersModel
from src.repo.base import BaseRepository
from src.schemas.users_schemas import User


class UsersRepository(BaseRepository):
    model = UsersModel
    schema = User