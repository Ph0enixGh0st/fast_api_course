from src.database import async_session_maker
from src.schemas.hotels_schemas import Hotel
from src.utils.db_manager import DBManager


async def test_add_hotel():
    hotel_data = Hotel(name="Test Hotel Name", location="Test Location Name")
    async with DBManager(session_factory=async_session_maker) as db:
        test_hotel = await db.hotels.add(hotel_data)