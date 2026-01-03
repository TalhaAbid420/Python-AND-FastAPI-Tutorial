from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    """
    This endpoint handles GET requests to the root path ('/').
    It returns a simple welcome message.
    """
    return {"message": "Hello World - This is a GET request example!"}

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app using Uvicorn
    # Go to http://127.0.0.1:8000 in your browser
    uvicorn.run(app, host="127.0.0.1", port=8000)

