from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.get("/")
async def ping():
    """A test ping endpoint."""
    return {"ping": "I'm alive!"}


@app.post("/process")
async def process_something(item: Optional[Item] = None):
    """Returns a list of the keys can values from the data you send."""
    return {
        "Your object": item.json() if item is not None else {},
        "JSON schema": Item.schema_json(),
    }


# Middleware added here
