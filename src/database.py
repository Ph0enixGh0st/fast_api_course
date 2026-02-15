from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool.impl import NullPool
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False  # change to True to see query in terminal
)

engine_null_pool = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    poolclass=NullPool
)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
async_session_maker_null_pool = async_sessionmaker(bind=engine_null_pool, expire_on_commit=False)

class BaseModel(DeclarativeBase):
    pass

#
# async def func():
#     async with engine.begin() as conn:
#         res = await conn.execute(text("SELECT version()"))
#         print("DB check...")
#         print(res.fetchone())
#
# asyncio.run(func())