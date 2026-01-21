from typing import Annotated

from fastapi import Depends, Query, HTTPException, Request
from pydantic import BaseModel

from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="Page number")]
    per_page: Annotated[int | None, Query(15, ge=1, lte=25, description="Results per page")]

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
