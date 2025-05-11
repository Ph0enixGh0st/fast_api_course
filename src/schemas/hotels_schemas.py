from typing import List

from pydantic import BaseModel, ConfigDict, Field


class Hotel(BaseModel):
    name: str
    location: str

class HotelPATCH(BaseModel):
    name: str | None = Field(None)
    location: str | None = Field(None)


class HotelsPrintOut(BaseModel):
    id: int
    name: str
    location: str

    model_config = ConfigDict(from_attributes=True)


class PaginatedHotelsPrintOut(BaseModel):
    page: int
    per_page: int
    total_found: int
    hotels: List[HotelsPrintOut]