from fastapi import FastAPI

app = FastAPI()

# Sample data (can be replaced with database interaction later)
user_data = {
    1: {"name": "Alice", "city": "New York"},
    2: {"name": "Bob", "city": "London"},
    3: {"name": "Charlie", "city": "Paris"}
}

@app.get("/users/{user_id}")
def get_user_by_id(user_id: int):
    """
    This endpoint demonstrates path parameters.
    It retrieves user data based on the `user_id` provided in the URL path.
    Example: Accessing /users/1 will return Alice's data.
    FastAPI automatically validates that user_id is an integer.
    """
    if user_id in user_data:
        return user_data[user_id]
    else:
        # Although not explicitly requested, returning a 404 is good practice
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app using Uvicorn
    # Test by visiting: http://127.0.0.1:8004/users/1 or http://127.0.0.1:8004/users/2
    # Check the interactive docs: http://127.0.0.1:8004/docs
    uvicorn.run(app, host="127.0.0.1", port=8004) # Use port 8004

