from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from src.database import async_session_maker
from src.models.users_models import UsersModel as UserModel

from src.schemas.users_schemas import UserRequestAdd, User

router = APIRouter(prefix="/auth", tags=["Authentication and authorisation"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/sign_up")
async def sign_up(
        user_data: UserRequestAdd
):
    async with async_session_maker() as session:
        hashed_password = pwd_context.hash(user_data.password)
        new_user = UserModel(email=user_data.email, hashed_password=hashed_password)

        session.add(new_user)
        try:
            await session.commit()
            await session.refresh(new_user)
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists."
            )

    return {"status": "success", "user_id": new_user.id, "email": new_user.email}