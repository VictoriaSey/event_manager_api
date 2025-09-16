from pymongo import MongoClient
import os




# connect to mongo atlas cluster
mongo_client = MongoClient(os.getenv("MONGO_URI"))


# Access database
event_manager_db = mongo_client["event_manager_db"]

# Pick a connection to operate on
events_collection = event_manager_db["events"]
users_collection = event_manager_db["users"]