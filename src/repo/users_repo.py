from http.client import HTTPException

from pydantic import EmailStr
from sqlalchemy import select

from src.models.users_models import UsersModel
from src.repo.base import BaseRepository
from src.schemas.users_schemas import User, UserHashedPassword


class UsersRepository(BaseRepository):
    model = UsersModel
    schema = User

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return UserHashedPassword.model_validate(model)
