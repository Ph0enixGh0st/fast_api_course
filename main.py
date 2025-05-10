import uvicorn
from typing import Dict

from fastapi import FastAPI, Query, Body, Path

from hotels import router as router_hotels

app = FastAPI()

app.include_router(router_hotels)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
