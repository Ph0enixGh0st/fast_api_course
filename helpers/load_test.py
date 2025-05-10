import asyncio
import time
import threading

from fastapi import FastAPI
import uvicorn

app = FastAPI(docs_url=None)


@app.get("/sync/{id}")
def sync_func(id: int):
    print(f"sync. Threads: {threading.active_count()}")
    print(f"sync. Started {id}: {time.time():.2f}")
    time.sleep(3)
    print(f"sync. Finished {id}: {time.time():.2f}")


@app.get("/async/{id}")
async def async_func(id: int):
    print(f"async. Threads: {threading.active_count()}")
    print(f"async. Started {id}: {time.time():.2f}")
    await asyncio.sleep(3)
    print(f"async. Finished {id}: {time.time():.2f}")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)