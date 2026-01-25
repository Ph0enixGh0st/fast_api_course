from fastapi import APIRouter, Body, Path, Query, HTTPException

from src.models.hotels_models import HotelsModel
from src.schemas.rooms_schemas import RoomCreate,  RoomUpdate, RoomPatch, RoomCreateInternal
from src.api.dependencies import DBSpawner


rooms_router = APIRouter(prefix="/rooms", tags=["Rooms - Standalone"])
hotels_rooms_router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Rooms via Hotels"])


@hotels_rooms_router.get("/search")
async def search_rooms(
    db: DBSpawner,
    hotel_id: int,
    name: str | None = Query(None, description="Name of the rooms"),
    description: str | None = Query(None, description="Description of the rooms")
):
    return await db.rooms.search_rooms(
        hotel_id=hotel_id,
        name=name,
        description=description
    )


@hotels_rooms_router.get("/{room_id}")
async def find_room_by_ids(
        db: DBSpawner,
        hotel_id: int,
        room_id: int
):
    filters = {"id": room_id, "hotel_id": hotel_id}
    room = await db.rooms.get_one_or_none(**filters)
    if not room:
        raise HTTPException(404, "Room not found")
    return room


@hotels_rooms_router.post("")
async def create_room(
    db: DBSpawner,
    hotel_id: int,
    room_data: RoomCreate = Body(openapi_examples={
        "1": {
            "summary": "Example 1",
            "value": {
                "name": "Test Room Name 1",
                "description": "Test Room Description 1",
                "price": 100500,
                "quantity": 5
                }
            },
        "2": {
            "summary": "Example 1",
            "value": {
                "name": "Test Room Name 2",
                "description": "Test Room Description 2",
                "price": 200,
                "quantity": 2
                }
            }
        }
    )
):

    # Verify hotel exists
    hotel = await db.session.get(HotelsModel, hotel_id)
    if not hotel:
        raise HTTPException(404, "Hotel not found")

    _room_data = room_data.model_dump()
    _room_data["hotel_id"] = hotel_id

    room = await db.rooms.add(
        RoomCreateInternal(**_room_data)
    )
    await db.commit()

    return {"status": "success", "created": room}


@hotels_rooms_router.put("/{room_id}")
async def edit_room(
        db: DBSpawner,
        hotel_id: int,
        room_id: int,
        room_data: RoomUpdate
):
    hotel = await db.session.get(HotelsModel, hotel_id)
    if not hotel:
        raise HTTPException(404, "Hotel not found")

    existing_room = await db.rooms.get_one_or_none(
        id=room_id,
        hotel_id=hotel_id
    )
    if not existing_room:
        raise HTTPException(404, "Room not found in this hotel")

    _room_data = RoomUpdate(
        hotel_id=hotel_id,
        **room_data.model_dump()
    )

    room = await db.rooms.edit(room_id, _room_data)
    await db.commit()

    return {"status": "success", "updated": room}


@rooms_router.get("/{room_id}")
async def get_room_by_id(
        db: DBSpawner,
        room_id: int
):
    return await db.rooms.get_one_or_none(
        id=room_id
    )


@rooms_router.delete("/{room_id}")
async def delete_room_by_id(
    db: DBSpawner,
    room_id: int = Path(description="ID of the room")
):

    deleted_room = await db.rooms.delete(room_id)
    if not deleted_room:
        raise HTTPException(404, "Room not found")
    await db.commit()

    return {"status": "success", "deleted": deleted_room}


@rooms_router.patch("/{room_id}")
async def partially_edit_room(
        db: DBSpawner,
        room_id: int,
        room_data: RoomPatch,
):
    existing_room = await db.rooms.get_one_or_none(id=room_id)
    if not existing_room:
        raise HTTPException(404, "Room not found")

    patch_data = room_data.model_dump(exclude_unset=True)
    room = await db.rooms.edit(room_id, RoomPatch(**patch_data))
    await db.commit()

    return {"status": "OK", "patched": room}
