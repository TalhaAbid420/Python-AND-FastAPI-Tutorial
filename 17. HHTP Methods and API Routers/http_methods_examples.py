from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Union, Dict, List

# Define a Pydantic model for the request body
class Item(BaseModel):
    name: str
    description: str | None = None  # Optional description
    price: float
    is_offer: bool | None = None  # Optional boolean

# New Pydantic model to include item_id in the response for GET requests
class ItemWithId(Item):
    item_id: int

app = FastAPI()

# In-memory storage for demonstration purposes, now centralized for all item operations
# We'll pre-populate it with some data for GET, PUT, and DELETE examples
items_db: Dict[int, Dict] = {
    1: {"name": "Laptop", "description": "Powerful computing machine", "price": 1200.0, "is_offer": False},
    2: {"name": "Mouse", "description": "Ergonomic wireless mouse", "price": 25.50, "is_offer": True},
    3: {"name": "Keyboard", "description": "Mechanical gaming keyboard", "price": 75.0, "is_offer": False},
    4: {"name": "Monitor", "description": "4K UHD display", "price": 350.0, "is_offer": True}
}

# --- GET Example (Root) ---
@app.get("/")
def read_root():
    """
    This endpoint handles GET requests to the root path ('/').
    It returns a simple welcome message.
    Access at http://127.0.0.1:8000
    """
    return {"message": "Hello World - This is a GET request example!"}

# --- GET Example (Retrieve All Items) ---
@app.get("/items/", response_model=List[ItemWithId]) # <--- Updated response_model
def get_all_items():
    """
    This endpoint handles GET requests to retrieve all items from the database.
    It returns a list of all items, including their IDs.
    Access at http://127.0.0.1:8000/items/
    """
    # Create a list of dictionaries, each including the item_id from the key
    return [{"item_id": item_id, **item_data} for item_id, item_data in items_db.items()]

# --- Path Parameter Example (GET a Specific Item) ---
@app.get("/items/{item_id}", response_model=ItemWithId) # <--- Updated response_model
def get_item_by_id(item_id: int):
    """
    This endpoint demonstrates path parameters, retrieving a specific item.
    It retrieves item data based on the `item_id` provided in the URL path.
    Example: Accessing http://127.0.0.1:8000/items/1 will return Laptop's data.
    FastAPI automatically validates that item_id is an integer.
    """
    if item_id in items_db:
        return {"item_id": item_id, **items_db[item_id]} # <--- Return item_id
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# --- POST Example ---
@app.post("/items/", response_model=ItemWithId) # <--- Updated response_model
def create_item(item: Item):
    """
    This endpoint handles POST requests to create a new item.
    It expects item data in the request body matching the Item model.
    It returns the created item data, including its new ID.
    Test via http://127.0.0.1:8000/docs (POST /items/)
    """
    # Generate a new item ID by taking the current number of items and adding 1
    # This is a simple in-memory ID generation, not suitable for production
    item_id = max(items_db.keys()) + 1 if items_db else 1

    # Store the item's data in the database (dictionary) using the generated ID
    items_db[item_id] = item.model_dump()

    # Return a response containing the new item ID along with the item's data
    return {"item_id": item_id, **item.model_dump()}

# --- PUT Example ---
@app.put("/items/{item_id}", response_model=ItemWithId) # <--- Updated response_model
def update_item(item_id: int, item: Item):
    """
    This endpoint handles PUT requests to update an existing item.
    It uses a path parameter `item_id` to identify the item.
    It expects the updated item data in the request body.
    If the item exists, it updates it completely; otherwise, returns a 404 error.
    Test via http://127.0.0.1:8000/docs (PUT /items/{item_id})
    """
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    items_db[item_id] = item.model_dump()
    return {"item_id": item_id, **item.model_dump()} # <--- Return item_id

# --- DELETE Example ---
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """
    This endpoint handles DELETE requests to remove an existing item.
    It uses a path parameter `item_id` to identify the item.
    If the item exists, it deletes it and returns a confirmation message.
    Otherwise, it returns a 404 error.
    Test via http://127.0.0.1:8000/docs (DELETE /items/{item_id})
    """
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    del items_db[item_id]
    return {"message": f"Item {item_id} deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app using Uvicorn on a single port.
    # Access all endpoints via http://127.0.0.1:8000
    # Check interactive docs at http://127.0.0.1:8000/docs
    uvicorn.run(app, host="127.0.0.1", port=8000)