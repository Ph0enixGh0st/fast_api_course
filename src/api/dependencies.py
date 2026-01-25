from typing import Annotated

from fastapi import Depends, Query, HTTPException, Request
from pydantic import BaseModel

from src.database import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager
from src.schemas.pagination import PaginationParams


PaginationSettings = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    access_token = request.cookies.get("access_token", None)
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not provided")
    return access_token

def get_current_user_id(access_token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(access_token)
    return data["user_id"]

CurrentUserId = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBSpawner = Annotated[DBManager, Depends(get_db)]