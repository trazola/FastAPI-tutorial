import asyncio
import datetime
from typing import Optional, List
from enum import Enum
from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Field

# initial app (run command: unicorn <name_file>:<name_instance_fast_api> --reload (only develop mode))

app = FastAPI()

# aync test


async def get_cd():
    print("start1")
    await asyncio.sleep(10)
    print("end1")
    return {}


async def get_cd2():
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
    b = await get_cd2()
    c = await get_cd3()
    end = datetime.datetime.now().time()
    return {"start": start, "end": end}


# URL parameters validate


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


# Order matters


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# Predefined values


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# Path parameters containing paths


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    print(file_path)
    return {"file_path": file_path}


# Query parameters

fake_products_db = [{"product_name": "Foo"}, {"product_name": "Bar"}, {"product_name": "Baz"}]


@app.get("/products/")
async def read_product(skip: int, limit: int = 10):
    return fake_products_db[skip : skip + limit]


# Optional parameters
@app.get("/products_two/")
async def read_product_2(skip: int, limit: int = 10, test: Optional[int] = None):
    return fake_products_db[skip : skip + limit]


# Multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item


# pydantic model


class Item(BaseModel):
    name: str
    desc: str
    price: float
    tax: float


@app.post(path="/items/", status_code=201)
async def create_item(item: Item):
    return item


# Request body + path parameters¶
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


# Additional validation
@app.get("/items_query/")
async def read_items_query(q: Optional[str] = Query(None, min_length=3, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Query parameter list / multiple values
@app.get("/items_multi/")
async def read_items_multi(q: Optional[List[str]] = Query(None)):
    query_items = {"q": q}
    return query_items


# Path Parameters and Numeric Validations
@app.get("/items_path/{item_id}")
async def read_items_path(
    item_id: int = Path(..., title="The ID of the item to get"),
    q: Optional[str] = Query(None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# Multiple body parameters


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


@app.put("/items_user/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


# Singular values in body
@app.put("/items_singular/{item_id}")
async def update_item_singular(
    *, item_id: int, item: Item = Body(..., embed=True), user: User, importance: int = Body(...)
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    print(results)
    return results


# Field pydantic
class Item2(BaseModel):
    name: str
    description: Optional[str] = Field(None, title="The description of the item", max_length=300)
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None


@app.put("/items_second/{item_id}")
async def update_item_second(item_id: int, item: Item2 = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
