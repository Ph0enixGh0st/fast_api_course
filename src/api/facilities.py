import json

from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationSettings, DBSpawner
from src.schemas.facilities_schemas import PaginatedFacilitiesPrintOut, Facility

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("", response_model=PaginatedFacilitiesPrintOut)
@cache(expire=10)
async def get_all_facilities(
        db: DBSpawner,
        pagination: PaginationSettings
):
    return await db.facilities.get_all_facilities(pagination)


@router.post("")
async def create_facility(
    db: DBSpawner,
    facility_data: Facility = Body(openapi_examples={
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
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "success", "created": facility}

