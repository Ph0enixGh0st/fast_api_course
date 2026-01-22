from fastapi import APIRouter, Body, Path, Query, HTTPException

from src.database import async_session_maker
from src.models.hotels_models import HotelsModel
from src.repo.rooms_repo import RoomsRepository
from src.schemas.rooms_schemas import Room, RoomCreate,  RoomUpdate, RoomPatch


router = APIRouter(prefix="/{hotel_id}/rooms", tags=["Rooms"])


@router.get("/search")
async def search_rooms(
    hotel_id: int,
    name: str | None = Query(None, description="Name of the rooms"),
    description: str | None = Query(None, description="Description of the rooms")
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).search_rooms(
            hotel_id=hotel_id,
            name=name,
            description=description
        )


@router.get("/{room_id}")
async def get_room(room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(
            id=room_id
        )


@router.delete("/{room_id}")
async def delete_room(
    room_id: int | None = Path(description="ID of the room")
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).delete(room_id)
        await session.commit()

    return {"status": "success", "deleted": room}


@router.post("")
async def create_room(
    room_data: RoomCreate = Body(openapi_examples={
        "1": {
            "summary": "Example 1",
            "value": {
                "hotel_id": 15,
                "name": "Test Room Name 1",
                "description": "Test Room Description 1",
                "price": 100500,
                "quantity": 5
                }
            },
        "2": {
            "summary": "Example 1",
            "value": {
                "hotel_id": 15,
                "name": "Test Room Name 2",
                "description": "Test Room Description 2",
                "price": 200,
                "quantity": 2
                }
            }
        }
    )
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()

    return {"status": "success", "created": room}

@router.put("/{room_id}")
async def update_room(
        room_id: int,
        room_data: RoomUpdate
):
    async with async_session_maker() as session:
        if room_data.hotel_id:
            hotel_exists = await session.get(HotelsModel, room_data.hotel_id)
            if not hotel_exists:
                raise HTTPException(status_code=404, detail="Hotel not found")

        room = await RoomsRepository(session).update(room_id, room_data)
        await session.commit()

    return {"status": "success", "updated": room}


@router.patch("/{room_id}")
async def patch_room(
        hotel_id: int,
        room_data: RoomPatch
):
    async with async_session_maker() as session:
        if room_data.hotel_id:
            hotel_exists = await session.get(HotelsModel, room_data.hotel_id)
            if not hotel_exists:
                raise HTTPException(status_code=404, detail="Hotel not found")

        room = await RoomsRepository(session).edit(hotel_id, room_data)
        await session.commit()

    return {"status": "success", "patched": room}
