from db import models
from db.database import engine
from fastapi import FastAPI
from routers import user, post, comment
from fastapi.staticfiles import StaticFiles
from auth import authentication
from fastapi.middleware.cors import CORSMiddleware


# Create FastAPI instance with title
app = FastAPI(
    title="API documentation",
)


# Include routers in the FastAPI instance
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)


# Define a route for the root URL
@app.get("/")
def index():
    return {"message": "Hello, World!"}


# Add CORS middleware to allow requests from the specified origins
origins = [
    'http://localhost:3000',
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create engine for the database
models.Base.metadata.create_all(bind=engine)


# Allow static files to be served from the /images directory
app.mount("/images", StaticFiles(directory="images"), name="images")
