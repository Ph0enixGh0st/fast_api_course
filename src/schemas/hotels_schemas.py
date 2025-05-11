from pydantic import BaseModel, Field


class Hotel(BaseModel):
    name: str
    location: str

class HotelPATCH(BaseModel):
    name: str | None = Field(None)
    location: str | None = Field(None)