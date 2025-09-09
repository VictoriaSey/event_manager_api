from fastapi import FastAPI, Form, File, UploadFile
from db import events_collection
from pydantic import BaseModel
from bson.objectid import ObjectId
from utils import replace_mongo_id
from typing import Annotated

tags_metadata = [
    {
       "name":"Home",
       "description": "Welcome to FastAPI",
    },
    {
        "name":"Events",
        "description":"Event list"},
    ]


class EventModel(BaseModel):
    title: str
    description: str


app = FastAPI(openapi_tags=tags_metadata)


@app.get("/", tags=["Home"])
def get_home():
    return {"message": "You are on the home page"}


# Event endpoints
@app.get("/events", tags=["Events"])
def get_events(title="", description="", limit=10, skip=0):
    # Get all events from database
    events = events_collection.find(
        filter={"$or":[
            {"title":{"$regex":title,"$options":"i"}},
            {"description":{"$regex":description,"$options":"i"}}]},
            limit=int(limit), 
            skip=int(skip)
    ).to_list()
    # Return response
    return {"data": list(map(replace_mongo_id, events))}


@app.post("/events", tags=["Events"])
def post_events(
    title: Annotated[str,Form()],
    description: Annotated[str,Form()],
    file: Annotated[UploadFile, File()]
    ):
 
    # Insert event into database
    # events_collection.insert_one(event.model_dump())
    # Return response
    return {"message": "Event added successfully"}


@app.get("/events/{event_id}",tags=["Events"])
def get_event_by_id(event_id):
    # Get event from database by id_
    event = events_collection.find_one({"_id": ObjectId(event_id)})
    # Return response
    return {"data": replace_mongo_id(event)}

@app.post("/uploadfile/")
def upload_file(file:UploadFile):
    return{"filename": file.filename}