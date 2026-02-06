from typing import List

from pydantic import BaseModel, ConfigDict, Field


class Facility(BaseModel):
    title: str
    description: str


class FacilitiesPrintOut(BaseModel):
    id: int
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class PaginatedFacilitiesPrintOut(BaseModel):
    """
    Represents a paginated list of facilities with metadata.
    Includes pagination details and a list of facility entries.
    """
    page: int
    per_page: int
    total_found: int
    facilities: List[FacilitiesPrintOut]


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityAdd):
    id: int
