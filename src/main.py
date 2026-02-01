import uvicorn
from fastapi import FastAPI

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as router_auth
from src.api.hotels import router as router_hotels
from src.api.rooms import hotels_rooms_router as router_hotel_rooms
from src.api.rooms import rooms_router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.amenities import router as router_amenities


app = FastAPI()

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_hotel_rooms)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_amenities)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, log_level="debug")
