from fastapi import FastAPI
from typing import Union # Or use Optional from typing

app = FastAPI()

# Sample data (can be replaced with database interaction later)
fake_items_db = [
    {"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"},
    {"item_name": "Qux"}, {"item_name": "Quux"}, {"item_name": "Corge"}
]

@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10, q: Union[str, None] = None):
    """
    This endpoint demonstrates query parameters.
    - `skip`: An integer query parameter with a default value of 0.
    - `limit`: An integer query parameter with a default value of 10.
    - `q`: An optional string query parameter (can be None).
    
    Query parameters are defined as function arguments that are NOT part of the path.
    They are used for things like pagination (skip, limit) or filtering (q).
    
    Examples:
    - /items/ -> uses defaults skip=0, limit=10
    - /items/?skip=2 -> skips first 2 items
    - /items/?limit=5 -> returns max 5 items
    - /items/?skip=1&limit=2 -> skips 1, returns next 2
    - /items/?q=Ba -> filters items containing 'Ba' (case-insensitive)
    """
    results = fake_items_db
    
    # Apply optional query parameter 'q' for filtering (simple example)
    if q:
        results = [item for item in results if q.lower() in item["item_name"].lower()]
        
    # Apply pagination using 'skip' and 'limit'
    paginated_results = results[skip : skip + limit]
    
    return {"query_params": {"skip": skip, "limit": limit, "q": q}, "items": paginated_results}

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app using Uvicorn
    # Test by visiting: 
    # http://127.0.0.1:8005/items/
    # http://127.0.0.1:8005/items/?skip=2&limit=2
    # http://127.0.0.1:8005/items/?q=baz
    # Check the interactive docs: http://127.0.0.1:8005/docs
    uvicorn.run(app, host="127.0.0.1", port=8005) # Use port 8005

