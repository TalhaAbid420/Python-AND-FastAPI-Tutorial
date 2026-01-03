from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Union

# 1. Create a "Department" (APIRouter) for Items
# Think of this as setting up a specific section of your shop,
# like the "Electronics" or "Books" aisle.
items_router = APIRouter()

# In-memory storage for items (just for demonstration)
# This data belongs to the "Items Department"
items_data: Dict[int, Dict] = {
    101: {"name": "Laptop", "price": 1200},
    102: {"name": "Headphones", "price": 150},
    103: {"name": "Mouse", "price": 30},
}

# Pydantic model for creating a new item
class Item(BaseModel):
    name: str
    price: float

# New Pydantic model to include item_id in the response
class ItemWithId(Item):
    item_id: int

# 2. Define Jobs (Endpoints) within this Department

# Get all items in this department
# When included in the main app with prefix="/items", this will be /items/
@items_router.get("/", response_model=Dict[str, Union[str, List[ItemWithId]]])
def get_all_items():
    """
    Get a list of all items in our shop, including their IDs.
    """
    # Iterate through items_data to include the item_id from the dictionary key
    items_list_with_ids = [{"item_id": item_id, **item_data} for item_id, item_data in items_data.items()]
    return {"message": "Here are all the items in our shop:", "items": items_list_with_ids}

# Get a specific item by its ID
# When included, this will be /items/{item_id}
@items_router.get("/{item_id}", response_model=ItemWithId)
def get_item(item_id: int):
    """
    Get details for a specific item using its ID.
    """
    if item_id in items_data:
        # Include item_id in the response for a single item
        return {"item_id": item_id, **items_data[item_id]}
    raise HTTPException(status_code=404, detail="Item not found in this department!")

# Add a new item to this department
# When included, this will be /items/
@items_router.post("/", response_model=Dict[str, Union[str, int, Item]])
def create_new_item(item: Item):
    """
    Add a brand new item to our shop.
    """
    new_id = max(items_data.keys()) + 1 if items_data else 201
    items_data[new_id] = item.dict()
    # The response should clearly indicate the new ID and the item data
    return {"message": f"Item '{item.name}' added successfully!", "item_id": new_id, **item.dict()}

# No uvicorn.run here! This file is a module, not a standalone app.