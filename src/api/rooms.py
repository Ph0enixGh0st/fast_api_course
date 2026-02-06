from datetime import date

from fastapi import APIRouter, Body, Path, Query, HTTPException

from src.models.hotels_models import HotelsModel
from src.schemas.amenities_schemas import RoomAmenityAdd
from src.schemas.facilities_schemas import RoomFacilityAdd
from src.schemas.rooms_schemas import RoomCreate, RoomUpdate, RoomPatch, RoomCreateInternal, Room, RoomUpdateInternal
from src.api.dependencies import DBSpawner


rooms_router = APIRouter(prefix="/rooms", tags=["Rooms - Standalone"])
hotels_rooms_router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Rooms via Hotels"])


@hotels_rooms_router.get("/search")
async def search_rooms(
    db: DBSpawner,
    hotel_id: int,
    date_from: date | None = Query(None, example="2026-01-01", description="Search availability of rooms with date from filter applied"),
    date_to: date | None = Query(None, example="2026-02-22", description="Search availability of rooms with date to filter applied")
):
    return await db.rooms.search_rooms(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to
    )


@hotels_rooms_router.get("/{room_id}", response_model=Room, response_model_exclude_none=True)
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
                "price_per_night": 100500,
                "quantity": 5,
                "facility_ids": [7, 11, 15],
                "amenity_ids": [1, 2, 3]
                }
            },
        "2": {
            "summary": "Example 1",
            "value": {
                "name": "Test Room Name 2",
                "description": "Test Room Description 2",
                "price_per_night": 200,
                "quantity": 2,
                "facility_ids": [7, 11, 15],
                "amenity_ids": [1, 2, 3]
                }
            }
        }
    )
):

    # Verify hotel exists
    hotel = await db.session.get(HotelsModel, hotel_id)
    if not hotel:
        raise HTTPException(404, "Hotel not found")

    _room_data = room_data.model_dump(exclude={"facility_ids", "amenity_ids"})
    _room_data["hotel_id"] = hotel_id

    room = await db.rooms.add(
        RoomCreateInternal(**_room_data)
    )

    room_facilities = [RoomFacilityAdd(room_id=room, facility_id=facility_id) for facility_id in room_data.facility_ids]
    room_amenities = [RoomAmenityAdd(room_id=room, amenity_id=amenity_id) for amenity_id in room_data.amenity_ids]
    await db.room_facilities.add_bulk(room_facilities)
    await db.room_amenities.add_bulk(room_amenities)

    await db.commit()

    return {"status": "success", "created": room}


@hotels_rooms_router.put("/{room_id}")
async def edit_room(
        db: DBSpawner,
        hotel_id: int,
        room_id: int,
        room_data: RoomUpdate = Body(...)
):
    hotel = await db.session.get(HotelsModel, hotel_id)
    if not hotel:
        raise HTTPException(404, "Hotel not found")

    existing_room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    if not existing_room:
        raise HTTPException(404, "Room not found in this hotel")

    if room_data.hotel_id != hotel_id:
        target_hotel = await db.session.get(HotelsModel, room_data.hotel_id)
        if not target_hotel:
            raise HTTPException(404, "Target hotel not found")

    _room_data = room_data.model_dump(exclude={"facility_ids", "amenity_ids"})
    room = await db.rooms.edit(room_id, RoomUpdateInternal(**_room_data))

    await db.room_facilities.delete_where(room_id=room_id)
    await db.room_amenities.delete_where(room_id=room_id)

    room_facilities = [RoomFacilityAdd(room_id=room_id, facility_id=fid) for fid in room_data.facility_ids]
    room_amenities = [RoomAmenityAdd(room_id=room_id, amenity_id=aid) for aid in room_data.amenity_ids]
    await db.room_facilities.add_bulk(room_facilities)
    await db.room_amenities.add_bulk(room_amenities)

    await db.commit()
    return {"status": "success", "updated": room}


@rooms_router.get("/{room_id}", response_model=Room, response_model_exclude_none=True)
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

    if "facility_ids" in patch_data:
        await db.room_facilities.delete_where(room_id=room_id)
        facilities = [RoomFacilityAdd(room_id=room_id, facility_id=fid) for fid in patch_data.pop("facility_ids")]
        await db.room_facilities.add_bulk(facilities)

    if "amenity_ids" in patch_data:
        await db.room_amenities.delete_where(room_id=room_id)
        amenities = [RoomAmenityAdd(room_id=room_id, amenity_id=aid) for aid in patch_data.pop("amenity_ids")]
        await db.room_amenities.add_bulk(amenities)

    if patch_data:  # remaining scalar fields
        room = await db.rooms.edit(room_id, RoomPatch(**patch_data))

    await db.commit()
    return {"status": "OK", "patched": room}
