from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Optional
from uuid import uuid4, UUID

app = FastAPI()

class Item(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., gt=0)

storage: Dict[UUID, Item] = {}

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    item_id = uuid4()
    storage[item_id] = item
    return {**item.dict(), "id": item_id}

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: UUID):
    if item_id not in storage:
        raise HTTPException(status_code=404, detail="Item not found")
    return {**storage[item_id].dict(), "id": item_id}

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: UUID, item: Item):
    if item_id not in storage:
        raise HTTPException(status_code=404, detail="Item not found")
    storage[item_id] = item
    return {**item.dict(), "id": item_id}

@app.delete("/items/{item_id}", response_model=Dict)
async def delete_item(item_id: UUID):
    if item_id not in storage:
        raise HTTPException(status_code=404, detail="Item not found")
    del storage[item_id]
    return {"message": "Item deleted successfully"}