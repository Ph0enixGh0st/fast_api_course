from fastapi import APIRouter, Body

from src.api.dependencies import PaginationSettings, DBSpawner
from src.schemas.amenities_schemas import PaginatedAmenitiesPrintOut, Amenity

router = APIRouter(prefix="/amenities", tags=["Amenities"])


@router.get("", response_model=PaginatedAmenitiesPrintOut)
async def get_all_amenities(
        db: DBSpawner,
        pagination: PaginationSettings
):
    return await db.amenities.get_all_amenities(pagination)


@router.post("")
async def create_amenity(
    db: DBSpawner,
    amenity_data: Amenity = Body(openapi_examples={
        "1": {
            "summary": "Example 1",
            "value": {
                "title": "Test Name 1",
                "description": "Test Description 1"
                }
            },
        "2": {
            "summary": "Example 2",
            "value": {
                "title": "Test Name 2",
                "description": "Test Description 2"
                }
            }
        }
    )
):
    amenity = await db.amenities.add(amenity_data)
    await db.commit()

    return {"status": "success", "created": amenity}

