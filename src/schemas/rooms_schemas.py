from pydantic import BaseModel, Field


class Room(BaseModel):
    """Represents a basic hotel with name and location."""
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    quantity: int


class RoomCreate(BaseModel):
    """Represents an addition of a room to an existing hotel."""
    hotel_id: int
    name: str
    description: str | None = Field(None)
    price: int
    quantity: int


class RoomUpdate(BaseModel):
    """Represents an update to an existing room, excluding its ID (PK)."""
    hotel_id: int = Field(ge=1)
    name: str
    description: str
    price: int = Field(ge=1)
    quantity: int = Field(ge=1)


class RoomPatch(BaseModel):
    """Represents a partial update to an existing room, excluding its ID (PK)."""
    hotel_id: int | None = Field(ge=1)
    name: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(ge=1)
    quantity: int | None = Field(ge=1)