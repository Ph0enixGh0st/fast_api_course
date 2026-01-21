from fastapi import APIRouter, HTTPException, status, Response, Request
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import CurrentUserId
from src.database import async_session_maker
from src.models.users_models import UsersModel as UserModel
from src.repo.users_repo import UsersRepository
from src.services.auth import AuthService
from src.schemas.users_schemas import UserRequestAdd


router = APIRouter(prefix="/auth", tags=["Authentication and authorisation"])


@router.post("/sign_up")
async def sign_up(
        user_data: UserRequestAdd
):
    async with async_session_maker() as session:
        hashed_password = AuthService().hash_password(user_data.password)
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


@router.post("/log_in")
async def log_in(
        user_data: UserRequestAdd,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=user_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User with this email is not registered."
            )
        if not AuthService().verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Wrong password."
            )
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.post("/log_out")
async def log_out(
        response: Response
):
        response.delete_cookie("access_token")
        return {"status": "OK"}

@router.get("/current_user")
async def get_current_user(
        user_id: CurrentUserId
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user
