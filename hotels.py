from fastapi import APIRouter, Body, HTTPException, Path, Query

from schemas.hotels_schemas import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Hotels"])


hotels = [
    {"id": 1, "city": "Houston, TX", "name": "Hilton"},
    {"id": 2, "city": "New York, NY", "name": "Marriott"},
    {"id": 3, "city": "Miami, FL", "name": "Four Seasons"},
    {"id": 4, "city": "New Jersey, NJ", "name": "Holiday Inn"},
    {"id": 5, "city": "Chicago, IL", "name": "Wyndham"},
    {"id": 6, "city": "Atlanta, GE", "name": "Hyatt"},
    {"id": 7, "city": "Mystic, CT", "name": "Harbor View Landing"},
    {"id": 8, "city": "West Hartford, CT", "name": "Delamar"},
    {"id": 9, "city": "North Conway, NH", "name": "Home2 Suites By Hilton"},
    {"id": 10, "city": "Plymouth, NH", "name": "Fairfield Inn & Suites by Marriott"},
]


@router.get("")
def get_hotels(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(5, ge=1, lt=15, description="Results per page")
):
    global hotels

    start = (page - 1) * per_page
    end = start + per_page

    paginated = hotels[start:end]

    return {
        "page": page,
        "per_page": per_page,
        "total": len(hotels),
        "hotels": paginated
    }


@router.get("/search")
def get_hotel(
    id: int | None = Query(None, description="ID of the hotel"),
    name: str | None = Query(None, description="Name of the hotel"),
    city: str | None = Query(None, description="City"),
    page: int = Query(1, ge=1, description="Page number (not allowed when searching by ID)"),
    per_page: int = Query(5, ge=1, lt=15, description="Results per page (not allowed when searching by ID)")
):
    if id is not None and (page != 1 or per_page != 5):
        raise HTTPException(
            status_code=400,
            detail="Pagination parameters `page` and `per_page` are not allowed when searching by `id`."
        )

    matches = hotels

    if id is not None:
        matches = [hotel for hotel in matches if hotel["id"] == id]
        return matches if matches else {"message": "No hotel found with that ID"}

    if name is not None:
        matches = [hotel for hotel in matches if name.lower() in hotel["name"].lower()]
    if city is not None:
        matches = [hotel for hotel in matches if city.lower() in hotel["city"].lower()]

    start = (page - 1) * per_page
    end = start + per_page
    paginated = matches[start:end]

    return {
        "page": page,
        "per_page": per_page,
        "total_found": len(matches),
        "returned": len(paginated),
        "hotels": paginated
    } if paginated else {"message": "No hotels found with your search criteria"}


@router.delete("/{hotel_id}")
def delete_hotel(
    hotel_id: int | None = Path(description="ID of the hotel")
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "success", "remaining": hotels}


@router.post("")
def create_hotel(
    hotel_data: Hotel = Body(openapi_examples={
        "1": {
            "summary": "Example 1",
            "value": {
                "name": "River Inn",
                "city": "Seaside, OR"
                }
            },
        "2": {
            "summary": "Example 2",
            "value": {
                "name": "Comfort Inn & Suites",
                "city": "Coeur d'Alene, ID"
                }
            }
        }
    )
):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1 if hotels else 1,
            "name": hotel_data.name,
            "city": hotel_data.city
        }
    )
    return {"status": "success", "name": hotel_data.name, "city": hotel_data.city}


@router.put("/{hotel_id}")
def put_hotel(
        hotel_id: int,
        hotel_data: Hotel
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            if hotel_data.city is not None:
                hotel["city"] = hotel_data.city
            return {"status": "success", "updated": hotel}
    return {"status": "error", "message": "Hotel not found"}



@router.patch("/{hotel_id}")
def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.name:
                hotel["name"] = hotel_data.name
            if hotel_data.city:
                hotel["city"] = hotel_data.city
            return {"status": "success", "updated": hotel}
    return {"status": "error", "message": "Hotel not found"}


@router.get("/")
def say_hi():
    return "Hi Hi Hi"