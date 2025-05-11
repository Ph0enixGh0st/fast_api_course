from typing import List, Annotated

from fastapi import APIRouter, Body, HTTPException, Path, Query

from sqlalchemy import delete, insert, select, func

from src.api.dependencies import PaginationSettings
from src.database import async_session_maker
from src.models.hotels_models import HotelsModel
from src.schemas.hotels_schemas import Hotel, HotelPATCH, HotelsPrintOut, PaginatedHotelsPrintOut

router = APIRouter(prefix="/hotels", tags=["Hotels"])


hotels = [
    {"id": 1, "city": "Houston, TX", "name": "Hilton"},
    {"id": 2, "city": "New York, NY", "name": "Marriott"},
    {"id": 3, "city": "Miami, FL", "name": "Four Seasons"},
    {"id": 4, "city": "New Jersey, NJ", "name": "Holiday Inn"},
    {"id": 5, "city": "Chicago, IL", "name": "Wyndham"},
    {"id": 6, "city": "Atlanta, GE", "name": "Hyatt"},
    {"id": 7, "city": "Mystic, CT", "name": "Harbor View Landing"},
    {"id": 8, "city": "West Hartford, CT", "name": "Delamar"},
    {"id": 9, "city": "North Conway, NH", "name": "Home2 Suites By Hilton"},
    {"id": 10, "city": "Plymouth, NH", "name": "Fairfield Inn & Suites by Marriott"},
]


@router.get("", response_model=PaginatedHotelsPrintOut)
async def get_hotels(pagination: PaginationSettings):
    async with async_session_maker() as session:
        total_query = select(func.count()).select_from(HotelsModel)
        total = await session.scalar(total_query)

        offset = (pagination.page - 1) * pagination.per_page
        query = select(HotelsModel).offset(offset).limit(pagination.per_page)
        result = await session.execute(query)
        hotels = result.scalars().all()

        return PaginatedHotelsPrintOut(
            page=pagination.page,
            per_page=pagination.per_page,
            total_found=total,
            hotels=hotels,
        )



@router.get("/search", response_model=PaginatedHotelsPrintOut | dict)
async def search_hotels(
    pagination: PaginationSettings,
    id: int | None = Query(None, description="ID of the hotel"),
    name: str | None = Query(None, description="Name of the hotel"),
    location: str | None = Query(None, description="Location of the hotel")
):
    async with async_session_maker() as session:
        # ID search (no pagination override)
        if id is not None:
            result = await session.execute(
                select(HotelsModel).where(HotelsModel.id == id)
            )
            hotel = result.scalar_one_or_none()
            if not hotel:
                return {"message": "No hotel found with given ID"}

            return PaginatedHotelsPrintOut(
                page=1,
                per_page=1,
                total_found=1,
                hotels=[hotel],
            )

        # Build base query with optional filters
        query = select(HotelsModel)
        if name:
            query = query.where(HotelsModel.name.ilike(f"%{name}%"))
        if location:
            query = query.where(HotelsModel.location.ilike(f"%{location}%"))

        # Count total results
        count_query = select(func.count()).select_from(query.subquery())
        total = await session.scalar(count_query)

        # Apply pagination
        query = query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)
        result = await session.execute(query)
        hotels = result.scalars().all()

        if not hotels:
            return {"message": "No hotels found with your search criteria"}

        return PaginatedHotelsPrintOut(
            page=pagination.page,
            per_page=pagination.per_page,
            total_found=total,
            hotels=hotels,
        )


@router.delete("/{hotel_id}")
def delete_hotel(
    hotel_id: int | None = Path(description="ID of the hotel")
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "success", "remaining": hotels}


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
        add_hotel_stmt = insert(HotelsModel).values(
            **hotel_data.model_dump()
        )
        # SQL query print out upon API endpoint execution (only in dev):
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "success", "created": hotel_data.name}


@router.put("/{hotel_id}")
def put_hotel(
        hotel_id: int,
        hotel_data: Hotel
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            if hotel_data.city is not None:
                hotel["location"] = hotel_data.location
            return {"status": "success", "updated": hotel}
    return {"status": "error", "message": "Hotel not found"}



@router.patch("/{hotel_id}")
def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.name:
                hotel["name"] = hotel_data.name
            if hotel_data.city:
                hotel["city"] = hotel_data.city
            return {"status": "success", "updated": hotel}
    return {"status": "error", "message": "Hotel not found"}


@router.get("/")
def say_hi():
    return "Hi Hi Hi"