from fastapi import APIRouter, Body, Path, Query

from src.api.dependencies import PaginationSettings
from src.database import async_session_maker
from src.repo.hotels_repo import HotelsRepository
from src.schemas.hotels_schemas import Hotel, HotelPatch, PaginatedHotelsPrintOut, HotelUpdate

router = APIRouter(prefix="/hotels", tags=["Hotels"])

@router.get("", response_model=PaginatedHotelsPrintOut)
async def get_all_hotels(pagination: PaginationSettings):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all_hotels(pagination)


@router.get("/search", response_model=PaginatedHotelsPrintOut | dict)
async def search_hotels(
    pagination: PaginationSettings,
    name: str | None = Query(None, description="Name of the hotel"),
    location: str | None = Query(None, description="Location of the hotel")
):
    async with async_session_maker() as session:
        return await HotelsRepository(session).search_hotels(
            pagination,
            location=location,
            name=name
        )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(
            id=hotel_id,
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
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "success", "created": hotel}

@router.put("/{hotel_id}")
async def update_hotel(
        hotel_id: int,
        hotel_data: HotelUpdate
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).update(hotel_id, hotel_data)
        await session.commit()

    return {"status": "success", "updated": hotel}


@router.patch("/{hotel_id}")
async def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPatch
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).edit(hotel_id, hotel_data)
        await session.commit()

    return {"status": "success", "patched": hotel}
