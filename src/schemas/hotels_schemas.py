from typing import List

from pydantic import BaseModel, ConfigDict, Field


class Hotel(BaseModel):
    """Represents a basic hotel with name and location."""
    name: str
    location: str


class HotelUpdate(BaseModel):
    """Represents an update to an existing hotel, including its ID."""
    id: int
    name: str
    location: str


class HotelPatch(BaseModel):
    """Represents a partial update to a hotel; all fields are optional."""
    name: str | None = Field(None)
    location: str | None = Field(None)


class HotelsPrintOut(BaseModel):
    """Represents the full output structure of a hotel, including ID."""
    id: int
    name: str
    location: str

    model_config = ConfigDict(from_attributes=True)


class PaginatedHotelsPrintOut(BaseModel):
    """
    Represents a paginated list of hotels with metadata.
    Includes pagination details and a list of hotel entries.
    """
    page: int
    per_page: int
    total_found: int
    hotels: List[HotelsPrintOut]
