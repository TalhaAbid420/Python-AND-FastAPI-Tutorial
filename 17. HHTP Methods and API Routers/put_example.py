from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Define a Pydantic model for the request body (same as POST example)
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    is_offer: bool | None = None

app = FastAPI()

# In-memory storage (pre-populate for demonstration)
items_db = {
    1: {"name": "Initial Item", "description": "An item to be updated", "price": 9.99, "is_offer": False}
}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """
    This endpoint handles PUT requests to update an existing item.
    It uses a path parameter `item_id` to identify the item.
    It expects the updated item data in the request body.
    If the item exists, it updates it completely; otherwise, returns a 404 error.
    """
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    items_db[item_id] = item.dict()
    return {"item_id": item_id, **item.dict()}

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app using Uvicorn
    # Test with curl: curl -X PUT "http://127.0.0.1:8002/items/1" -H "Content-Type: application/json" -d 
    #                 '{"name": "Updated Item", "price": 10.99}'
    # Or use FastAPI docs: http://127.0.0.1:8002/docs
    uvicorn.run(app, host="127.0.0.1", port=8002) # Use port 8002

