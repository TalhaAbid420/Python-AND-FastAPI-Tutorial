from fastapi import FastAPI
from pydantic import BaseModel

# Define a Pydantic model for the request body
class Item(BaseModel):
    name: str
    description: str | None = None # Optional description
    price: float
    is_offer: bool | None = None # Optional boolean

app = FastAPI()

# In-memory storage (for demonstration purposes)
items_db = {}

@app.post("/items/")
def create_item(item: Item):
    """
    This endpoint handles POST requests to create a new item.
    It expects item data in the request body matching the Item model.
    It returns the created item data.
    """
    # Generate a new item ID by taking the current number of items and adding 1
    item_id = len(items_db) + 1  # Simple ID generation

    # Store the item's data in the database (dictionary) using the generated ID
    items_db[item_id] = item.model_dump()

    # Return a response containing the new item ID along with the item's data
    return {"item_id": item_id, **item.model_dump()}


if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app using Uvicorn
    # You can test this using tools like curl or Postman, or FastAPI's interactive docs at http://127.0.0.1:8001/docs
    uvicorn.run(app, host="127.0.0.1", port=8001) # Use a different port to avoid conflict if running others

