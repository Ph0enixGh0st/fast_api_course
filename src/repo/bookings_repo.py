from sqlalchemy import select, func
from pydantic import BaseModel
from typing import List

from src.models.bookings_models import BookingsModel
from src.schemas.bookings_schemas import BookingsPrintOut
from src.schemas.pagination import PaginationParams
from src.repo.base import BaseRepository
from src.schemas.hotels_schemas import HotelsPrintOut, PaginatedHotelsPrintOut


class BookingsRepository(BaseRepository):
    """
       Repository for bookings data operations.

       ⚠️NOTE: When defining routes that use this repository, place specific paths
       (like '/search') BEFORE parametric paths (like '/{hotel_id}') to avoid routing conflicts.
    """
    model = BookingsModel
    schema = BookingsPrintOut

    async def get_all_bookings(self, pagination: PaginationParams):
        total_query = select(func.count()).select_from(BookingsModel)
        total = await self.session.scalar(total_query)

        offset = (pagination.page - 1) * pagination.per_page
        query = select(BookingsModel).order_by(BookingsModel.id).offset(offset).limit(pagination.per_page)
        result = await self.session.execute(query)
        bookings = result.scalars().all()

        return PaginatedBookingsPrintOut(
            page=pagination.page,
            per_page=pagination.per_page,
            total_found=total,
            bookings=bookings,
        )


    async def get_bookings_current_user(self, user_id: int, pagination: PaginationParams):
        total_query = select(func.count()).select_from(BookingsModel).where(BookingsModel.user_id == user_id)
        total = await self.session.scalar(total_query)

        offset = (pagination.page - 1) * pagination.per_page
        query = select(BookingsModel).where(BookingsModel.user_id == user_id).order_by(BookingsModel.id).offset(offset).limit(pagination.per_page)
        result = await self.session.execute(query)
        bookings = result.scalars().all()

        return PaginatedBookingsPrintOut(
            page=pagination.page,
            per_page=pagination.per_page,
            total_found=total,
            bookings=[BookingsPrintOut.model_validate(b) for b in bookings],
        )


class PaginatedBookingsPrintOut(BaseModel):
    """
    Represents a paginated list of bookings with metadata.
    """
    page: int
    per_page: int
    total_found: int
    bookings: List[BookingsPrintOut]
