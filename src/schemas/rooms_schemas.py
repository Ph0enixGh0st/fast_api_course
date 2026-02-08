from pydantic import BaseModel, Field, ConfigDict


class Room(BaseModel):
    """Represents a basic hotel with name and location."""
    id: int
    hotel_id: int
    name: str
    description: str | None = Field(None)
    price_per_night: int
    quantity: int
    rooms_left: int | None = Field(None)

    model_config = ConfigDict(from_attributes=True)


class RoomCreate(BaseModel):
    """Represents an addition of a room to an existing hotel."""
    name: str
    description: str | None = Field(None)
    price_per_night: int
    quantity: int
    facility_ids: list[int] | None = Field(default=None)
    amenity_ids: list[int] | None = Field(default=None)


class RoomCreateInternal(BaseModel):
    """Internal use - includes hotel_id, excludes relation IDs"""
    hotel_id: int
    name: str
    description: str | None = Field(None)
    price_per_night: int
    quantity: int


class RoomUpdate(BaseModel):
    """Represents an update to an existing room, excluding its ID (PK)."""
    new_hotel_id: int
    name: str
    description: str
    price_per_night: int = Field(ge=1)
    quantity: int = Field(ge=1)
    facility_ids: list[int]
    amenity_ids: list[int]


class RoomUpdateInternal(BaseModel):
    hotel_id: int
    name: str
    description: str
    price_per_night: int
    quantity: int


class RoomPatch(BaseModel):
    """Represents a partial update to an existing room, excluding its ID (PK)."""
    hotel_id: int | None = Field(default=None, ge=1)
    name: str | None = Field(None)
    description: str | None = Field(None)
    price_per_night: int | None = Field(default=None, ge=1)
    quantity: int | None = Field(default=None, ge=1)
    facility_ids: list[int] | None = Field(default=None)
    amenity_ids: list[int] | None = Field(default=None)
