import asyncio
import datetime

from fastapi import FastAPI

app = FastAPI()

async def get_cd():
    print("start1")
    await asyncio.sleep(10)
    print("end1")
    return {}

def get_cd2():
    print("start2")
    for x in range(1, 1000000000):
        pass
    print("end2")
    return {}

async def get_cd3():
    print("start3")
    await asyncio.sleep(10)
    print("end3")
    return {}

@app.get("/")
async def root():
    start = datetime.datetime.now().time()
    a = await get_cd()
    b = get_cd2()
    c = await get_cd3()
    end = datetime.datetime.now().time()
    return {
        "start": start,
        "end": end
    }