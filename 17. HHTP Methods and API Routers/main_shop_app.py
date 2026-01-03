from fastapi import FastAPI
from shop_items_router import items_router # <--- IMPORT the "Items Department"

# 1. Create the Main Shop (FastAPI application)
# This is like the main entrance and management of your entire online shop.
app = FastAPI(title="My Awesome Online Shop API")

# 2. Set up the Departments on the Main Shop Floor
# "Plug in" the Items Department into the main shop.
# - prefix="/items": Means all endpoints in `items_router` will start with /items.
#   So, / in items_router becomes /items/, and /{item_id} becomes /items/{item_id}.
# - tags=["Shop Items"]: Helps organize the interactive API documentation (Swagger UI).
app.include_router(items_router, prefix="/items", tags=["Shop Items"])


# 3. Define Main Shop Endpoints (if any)
# These are general shop-level announcements or services.
@app.get("/")
def read_root():
    """
    Welcome message for the main shop entrance.
    """
    return {"message": "Welcome to My Awesome Online Shop API! Check out /items/"}

@app.get("/about/")
def about_shop():
    """
    Information about the shop.
    """
    return {"message": "This is a demo online shop built with FastAPI!"}


# 4. Run the Main Shop
if __name__ == "__main__":
    import uvicorn
    print("Starting the main shop API on http://127.0.0.1:8000")
    print("Check items at: http://127.0.0.1:8000/items/")
    print("Check specific item: http://127.0.0.1:8000/items/101")
    print("See interactive docs at: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8006)