from fastapi import FastAPI, HTTPException

app = FastAPI()

# In-memory storage (pre-populate for demonstration)
items_db = {
    1: {"name": "Item One", "description": "This is item one"},
    2: {"name": "Item Two", "description": "This is item two"}
}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """
    This endpoint handles DELETE requests to remove an existing item.
    It uses a path parameter `item_id` to identify the item.
    If the item exists, it deletes it and returns a confirmation message.
    Otherwise, it returns a 404 error.
    """
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    del items_db[item_id]
    return {"message": f"Item {item_id} deleted successfully"}

@app.get("/items/") # Add a way to see remaining items
def get_items():
    return items_db

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app using Uvicorn
    # Test with curl: curl -X DELETE "http://127.0.0.1:8003/items/1"
    # Check remaining items: curl "http://127.0.0.1:8003/items/"
    # Or use FastAPI docs: http://127.0.0.1:8003/docs
    uvicorn.run(app, host="127.0.0.1", port=8003) # Use port 8003

