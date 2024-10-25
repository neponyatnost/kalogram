from fastapi import FastAPI


# Create FastAPI instance with title and description
app = FastAPI(
    title="API documentation",
)


# Define a route for the root URL
@app.get("/")
def index():
    return {"message": "Hello, World!"}