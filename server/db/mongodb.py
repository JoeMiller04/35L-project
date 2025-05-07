from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "35L-project")
MONGO_DETAILS = "mongodb://localhost:27017" 

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

async_client = AsyncIOMotorClient(MONGO_DETAILS)
async_db = async_client[DATABASE_NAME]
users_collection = async_db.get_collection("users")
course_collection = async_db.get_collection("courses")

def get_collection(collection_name):
    return db[collection_name]

def create_document(collection_name, document):
    collection = get_collection(collection_name)
    result = collection.insert_one(document)
    return str(result.inserted_id)

def read_document(collection_name, document_id):
    collection = get_collection(collection_name)
    return collection.find_one({"_id": ObjectId(document_id)})

def update_document(collection_name, document_id, update_fields):
    collection = get_collection(collection_name)
    result = collection.update_one({"_id": ObjectId(document_id)}, {"$set": update_fields})
    return result.modified_count

def delete_document(collection_name, document_id):
    collection = get_collection(collection_name)
    result = collection.delete_one({"_id": ObjectId(document_id)})
    return result.deleted_count

def list_documents(collection_name):
    collection = get_collection(collection_name)
    return list(collection.find())

def get_db():
    return async_db