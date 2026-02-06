from typing import List

from pydantic import BaseModel, ConfigDict, Field


class Amenity(BaseModel):
    title: str
    description: str


class AmenitiesPrintOut(BaseModel):
    id: int
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class PaginatedAmenitiesPrintOut(BaseModel):
    """
    Represents a paginated list of amenities with metadata.
    Includes pagination details and a list of amenity entries.
    """
    page: int
    per_page: int
    total_found: int
    amenities: List[AmenitiesPrintOut]


class RoomAmenityAdd(BaseModel):
    room_id: int
    amenity_id: int


class RoomAmenity(RoomAmenityAdd):
    id: int
