from datetime import date

from fastapi import APIRouter, Body, Path, Query, HTTPException

from src.api.dependencies import PaginationSettings, DBSpawner
from src.schemas.hotels_schemas import Hotel, HotelPatch, PaginatedHotelsPrintOut, HotelUpdate


router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("", response_model=PaginatedHotelsPrintOut, response_model_exclude_none=True)
async def get_all_hotels(
        db: DBSpawner,
        pagination: PaginationSettings
):
    return await db.hotels.get_all_hotels(pagination)


@router.get("/search", summary="Search available hotels", response_model=PaginatedHotelsPrintOut | dict)
async def search_hotels(
    pagination: PaginationSettings,
    db: DBSpawner,
    name: str | None = Query(None, description="Name of the hotel"),
    location: str | None = Query(None, description="Location of the hotel"),
    date_from: date | None = Query(None, example="2026-01-11"),
    date_to: date | None = Query(None, example="2026-02-22"),
):
    if (date_from is None) != (date_to is None):
        raise HTTPException(422, "Both date_from and date_to must be provided together")
    return await db.hotels.search_hotels(
        pagination,
        location=location,
        name=name,
        date_to=date_to,
        date_from=date_from,
    )


@router.get("/{hotel_id}", summary="Get hotel by ID")
async def get_hotel(
        hotel_id: int,
        db: DBSpawner
):
        hotel = await db.hotels.get_one_or_none(id=hotel_id)
        if not hotel:
            raise HTTPException(404, "Hotel not found")
        rooms = await db.rooms.get_filtered(hotel_id=hotel_id)

        return {"hotel": hotel, "rooms": rooms}


@router.delete("/{hotel_id}")
async def delete_hotel(
    db: DBSpawner,
    hotel_id: int | None = Path(description="ID of the hotel"),
):
    deleted_hotel = await db.hotels.delete(hotel_id)
    if not deleted_hotel:
        raise HTTPException(404, "Hotel not found")
    await db.commit()
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
    await db.commit()
    return {"status": "success", "created": hotel}


@router.put("/{hotel_id}")
async def update_hotel(
        db: DBSpawner,
        hotel_id: int,
        hotel_data: HotelUpdate
):
    hotel = await db.hotels.update(hotel_id, hotel_data)
    await db.commit()
    return {"status": "success", "updated": hotel}


@router.patch("/{hotel_id}")
async def patch_hotel(
        db: DBSpawner,
        hotel_id: int,
        hotel_data: HotelPatch
):
    hotel = await db.hotels.edit(hotel_id, hotel_data)
    await db.commit()
    return {"status": "success", "patched": hotel}
