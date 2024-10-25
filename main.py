from db import models
from db.database import engine
from fastapi import FastAPI
from routers import user


# Create FastAPI instance with title and description
app = FastAPI(
    title="API documentation",
)


# Include routers in the FastAPI instance
app.include_router(user.router)


# Define a route for the root URL
@app.get("/")
def index():
    return {"message": "Hello, World!"}


# Create engine for the database
models.Base.metadata.create_all(bind=engine)