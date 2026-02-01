from fastapi import APIRouter, Body, Path, Query, HTTPException

from src.api.dependencies import PaginationSettings, DBSpawner
from src.schemas.hotels_schemas import Hotel, HotelPatch, PaginatedHotelsPrintOut, HotelUpdate


router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("", response_model=PaginatedHotelsPrintOut)
async def get_all_hotels(
        db: DBSpawner,
        pagination: PaginationSettings
):
    return await db.hotels.get_all_hotels(pagination)


@router.get("/search", summary="Get hotel(s) by name and/or location", response_model=PaginatedHotelsPrintOut | dict)
async def search_hotels(
    pagination: PaginationSettings,
    db: DBSpawner,
    name: str | None = Query(None, description="Name of the hotel"),
    location: str | None = Query(None, description="Location of the hotel")
):
    return await db.hotels.search_hotels(
        pagination,
        location=location,
        name=name
    )


@router.get("/{hotel_id}", summary="Get hotel by ID")
async def get_hotel(
        hotel_id: int,
        db: DBSpawner
):
        hotel = await db.hotels.get_one_or_none(id=hotel_id)
        rooms = await db.rooms.search_rooms(hotel_id=hotel_id)

        return {"hotel": hotel, "rooms": rooms}


@router.delete("/{hotel_id}")
async def delete_hotel(
    db: DBSpawner,
    hotel_id: int | None = Path(description="ID of the hotel"),
):
    deleted_hotel = await db.hotels.delete(hotel_id)
    if not deleted_hotel:
        raise HTTPException(404, "Hotel not found")

    return {"status": "success", "deleted": deleted_hotel}


@router.post("")
async def create_hotel(
    db: DBSpawner,
    hotel_data: Hotel = Body(openapi_examples={
        "1": {
            "summary": "Example 1",
            "value": {
                "name": "Test Name 1",
                "location": "Test Location 1"
                }
            },
        "2": {
            "summary": "Example 2",
            "value": {
                "name": "Test Name 2",
                "location": "Test Location 2"
                }
            }
        }
    )
):
    hotel = await db.hotels.add(hotel_data)

    return {"status": "success", "created": hotel}


@router.put("/{hotel_id}")
async def update_hotel(
        db: DBSpawner,
        hotel_id: int,
        hotel_data: HotelUpdate
):
    hotel = await db.hotels.update(hotel_id, hotel_data)

    return {"status": "success", "updated": hotel}


@router.patch("/{hotel_id}")
async def patch_hotel(
        db: DBSpawner,
        hotel_id: int,
        hotel_data: HotelPatch
):
    hotel = await db.hotels.edit(hotel_id, hotel_data)

    return {"status": "success", "patched": hotel}
