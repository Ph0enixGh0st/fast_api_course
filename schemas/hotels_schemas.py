from pydantic import BaseModel, Field


class Hotel(BaseModel):
    name: str
    city: str

class HotelPATCH(BaseModel):
    name: str | None = Field(None)
    city: str | None = Field(None)