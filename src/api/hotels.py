from typing import List, Annotated

from fastapi import APIRouter, Body, HTTPException, Path, Query

from sqlalchemy import delete, insert, select, func

from src.api.dependencies import PaginationSettings
from src.database import async_session_maker, engine
from src.models.hotels_models import HotelsModel
from src.repo.hotels_repo import HotelsRepository
from src.schemas.hotels_schemas import Hotel, HotelPatch, HotelsPrintOut, PaginatedHotelsPrintOut, HotelUpdate

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("", response_model=PaginatedHotelsPrintOut)
async def get_all_hotels(pagination: PaginationSettings):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all_hotels(pagination)


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(
            id=hotel_id,
        )


@router.get("/search", response_model=PaginatedHotelsPrintOut | dict)
async def search_hotels(
    pagination: PaginationSettings,
    hotel_id: int | None = Query(None, description="ID of the hotel"),
    name: str | None = Query(None, description="Name of the hotel"),
    location: str | None = Query(None, description="Location of the hotel")
):
    async with async_session_maker() as session:
        return await HotelsRepository(session).search_hotels(
            pagination,
            id=hotel_id,
            location=location,
            name=name
        )


@router.delete("/{hotel_id}")
async def delete_hotel(
    hotel_id: int | None = Path(description="ID of the hotel")
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).delete(hotel_id)
        await session.commit()

    return {"status": "success", "deleted": hotel}


@router.post("")
async def create_hotel(
    hotel_data: Hotel = Body(openapi_examples={
        "1": {
            "summary": "Example 1",
            "value": {
                "name": "River Inn",
                "location": "Seaside, OR"
                }
            },
        "2": {
            "summary": "Example 2",
            "value": {
                "name": "Comfort Inn & Suites",
                "location": "Coeur d'Alene, ID"
                }
            }
        }
    )
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    # return {"status": "success", "created": hotel_data.name, "location": hotel_data.location}
    return {"status": "success", "created": hotel}

@router.put("/{hotel_id}")
async def update_hotel(
        hotel_id: int,
        hotel_data: HotelUpdate
):
    async with async_session_maker() as session:
        hotel_data.id = hotel_id
        hotel = await HotelsRepository(session).update(hotel_id, hotel_data)
        await session.commit()

    return {"status": "success", "updated": hotel}


@router.patch("/{hotel_id}")
def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPatch
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.name:
                hotel["name"] = hotel_data.name
            if hotel_data.city:
                hotel["city"] = hotel_data.city
            return {"status": "success", "patched": hotel}
    return {"status": "error", "message": "Hotel not found"}


@router.get("/")
def say_hi():
    return "Hi Hi Hi"