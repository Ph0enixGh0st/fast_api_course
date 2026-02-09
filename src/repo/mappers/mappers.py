from sqlalchemy import inspect

from src.models.hotels_models import HotelsModel
from src.models.rooms_models import RoomsModel
from src.repo.mappers.base import DataMapper
from src.schemas.hotels_schemas import Hotel, HotelsPrintOut, HotelsPrintOutWithRooms
from src.schemas.rooms_schemas import Room, RoomWithRelations


def is_loaded(obj, attr: str) -> bool:
    """Check if a relationship is loaded without triggering lazy load."""
    return attr not in inspect(obj).unloaded


class HotelDataMapper(DataMapper):
    db_model = HotelsModel
    schema = Hotel


class HotelsPrintOutMapper(DataMapper):
    db_model = HotelsModel
    schema = HotelsPrintOut


class HotelWithRoomsMapper(DataMapper):
    db_model = HotelsModel
    schema = HotelsPrintOutWithRooms

    @classmethod
    def map_to_domain_entity(cls, data, **extra):
        # Build dict manually to avoid accessing lazy-loaded relationships
        hotel_dict = {
            "id": data.id,
            "name": data.name,
            "location": data.location,
        }
        hotel_dict.update(extra)
        return cls.schema.model_validate(hotel_dict)


class RoomMapper(DataMapper):
    db_model = RoomsModel
    schema = Room


class RoomWithRelationsMapper(DataMapper):
    db_model = RoomsModel
    schema = RoomWithRelations

    @classmethod
    def map_to_domain_entity(cls, data, **extra):
        # Build dict manually to avoid accessing lazy-loaded relationships
        room_dict = {
            "id": data.id,
            "hotel_id": data.hotel_id,
            "name": data.name,
            "description": data.description,
            "price_per_night": data.price_per_night,
            "quantity": data.quantity,
            "facilities": data.facilities if is_loaded(data, "facilities") else None,
            "amenities": data.amenities if is_loaded(data, "amenities") else None,
            "hotel": data.hotel if is_loaded(data, "hotel") else None,
        }
        room_dict.update(extra)
        return cls.schema.model_validate(room_dict)
