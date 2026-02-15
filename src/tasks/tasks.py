from PIL import Image
import os
import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings
from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager


@celery_instance.task(name="resize_image")
def resize_image(image_path: str):
    sizes = [1000, 500, 200]
    output_folder = 'src/static/images'

    img = Image.open(image_path)

    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    for size in sizes:
        img_resized = img.resize((size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS)

        new_file_name = f"{name}_{size}px{ext}"

        output_path = os.path.join(output_folder, new_file_name)

        img_resized.save(output_path)

    print(f"Image saved with following sizes: {sizes} into {output_folder}")


async def get_todays_checkins_helper():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_todays_checkins()
        print(bookings)
        return bookings


@celery_instance.task(name="notify_today_checkins")
def notify_today_checkins():
    asyncio.run(get_todays_checkins_helper())