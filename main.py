from fastapi import FastAPI
import os
import cloudinary
from route.events import events_router
from route.users import users_router
from dotenv import load_dotenv

load_dotenv()

# Configure cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
)

tags_metadata = [
    {
        "name": "Home",
        "description": "Welcome to FastAPI",
    },
    {"name": "Events", "description": "Event list"},
]

app = FastAPI(
    title="Event Manager API",
    description="An API for managing events",
    openapi_tags=tags_metadata)


@app.get("/", tags=["Home"])
def get_home():
    return {"message": "You are on the home page"}


# include routers
app.include_router(events_router)

app.include_router(users_router)