from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="Page number")]
    per_page: Annotated[int | None, Query(15, ge=1, lte=25, description="Results per page")]

PaginationSettings = Annotated[PaginationParams, Depends()]
