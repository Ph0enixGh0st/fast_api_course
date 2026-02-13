import json

from fastapi import APIRouter, Body

from src.init import redis_connector
from src.api.dependencies import PaginationSettings, DBSpawner
from src.schemas.facilities_schemas import PaginatedFacilitiesPrintOut, Facility

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("", response_model=PaginatedFacilitiesPrintOut)
async def get_all_facilities(
        db: DBSpawner,
        pagination: PaginationSettings
):
    cached_facilities = await redis_connector.get("facilities")
    if not cached_facilities:
        facilities = await db.facilities.get_all_facilities(pagination)
        facilities_json = json.dumps(facilities.model_dump())
        await redis_connector.set("facilities", facilities_json, 15)

        return facilities
    else:
        return json.loads(cached_facilities)


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

