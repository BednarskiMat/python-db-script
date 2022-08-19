from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union

import tester
from mock_db import MockDb

item_db = MockDb({})

app = FastAPI()


#item class for posts 
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


# routes 
@app.get("/item")
async def get_item():
    return item_db.get_items()




@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    item_db.set_items(item.dict())
    return item_dict