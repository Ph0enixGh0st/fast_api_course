import json

import pytest

from httpx import ASGITransport, AsyncClient
from src.main import app

from src.config import settings
from src.database import BaseModel, engine_null_pool, async_session_maker_null_pool
from src.models import *
from src.schemas import *
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def async_main():
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def sign_up(async_main):
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        await ac.post(
            "/auth/sign_up",
            json={
                "email": "test_signup@test-signup.com",
                "password": "test_pwd"
            }
        )

@pytest.fixture(scope="session", autouse=True)
async def populate_db(sign_up):
    with open("tests/mock_hotels.json") as file:
        hotels = json.load(file)
    with open("tests/mock_rooms.json") as file:
        rooms = json.load(file)

    hotels = [HotelUpdate.model_validate(hotel) for hotel in hotels]
    rooms = [RoomCreateInternal.model_validate(room) for room in rooms]

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(hotels)
        await db.rooms.add_bulk(rooms)
        await db.commit()
