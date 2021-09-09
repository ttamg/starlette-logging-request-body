import logging
from typing import Optional

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
from starlette_logging_request_body.router import (
    BaseContextRoute,
    LogContextRoute,
    ObfuscatedRequestContextRoute,
)

# Initialise logging INFO level
logging.basicConfig(level=logging.INFO)

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


router = APIRouter(route_class=ObfuscatedRequestContextRoute)


@router.get("/")
async def ping():
    """A test ping endpoint."""
    return {"ping": "I'm alive!"}


@router.post("/process")
async def process_something(item: Optional[Item] = None):
    """Returns a list of the keys can values from the data you send."""
    return {
        "success": True,
        "JSON schema": Item.schema_json(),
    }


app.include_router(router)

