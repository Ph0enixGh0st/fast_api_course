from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="Page number")]
    per_page: Annotated[int | None, Query(5, ge=1, lt=15, description="Results per page")]

PaginationSettings = Annotated[PaginationParams, Depends()]
