import uvicorn
from typing import Dict

from fastapi import FastAPI, Query, Body, Path

app = FastAPI()


# It seems a bit off to use title and name, so I decided to add city instead
hotels = [
    {"id": 1, "city": "Houston, TX", "name": "Hilton"},
    {"id": 2, "city": "New York, NY", "name": "Marriott"},
    {"id": 3, "city": "Miami, FL", "name": "Four Seasons"},
    {"id": 4, "city": "New Jersey, NJ", "name": "Holiday Inn"},
    {"id": 5, "city": "Chicago, IL", "name": "Wyndham"},
    {"id": 6, "city": "Atlanta, GE", "name": "Hyatt"}
]


@app.get("/hotels")
def get_all_hotels():
    global hotels
    return hotels

@app.get("/hotels/{id}")
def get_hotel(
        id:int | None = Path(description="ID of the hotel"),
        name:str | None = Query(description="Name of the hotel")
):
    matches = hotels
    if id is not None:
        matches = [hotel for hotel in matches if hotel["id"] == id]
    if name is not None:
        matches = [hotel for hotel in matches if hotel["name"] == name]

    return matches if matches else {"message": "No hotel found with your search criteria"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(
    hotel_id: int | None = Path(description="ID of the hotel")
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "success", "remaining": hotels}


@app.post("/hotels")
def create_hotel(
    name:str = Body(..., embed=True)
):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1 if hotels else 1,
            "name": name
        }
    )
    return {"status": "success", "created": name}


@app.put("/hotels/{hotel_id}")
def put_hotel(
        hotel_id:int = Path(..., description="ID of the hotel to update"),
        city:str = Body(..., embed=True),
        name:str = Body(..., embed=True)
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if name is not None:
                hotel["name"] = name
            if city is not None:
                hotel["city"] = city
            return {"status": "success", "updated": hotel}
    return {"status": "error", "message": "Hotel not found"}



@app.patch("/hotels/{hotel_id}")
def patch_hotel(
        hotel_id:int | None = Path(description="ID of the hotel to patch"),
        data: Dict[str, str] = Body(
            ...,
            example={"city": "City to update", "name": "Name to update"}
        )
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if "name" in data:
                hotel["name"] = data["name"]
            if "city" in data:
                hotel["city"] = data["city"]
            return {"status": "success", "updated": hotel}
    return {"status": "error", "message": "Hotel not found"}


@app.get("/")
def say_hi():
    return "Hi Hi Hi"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
