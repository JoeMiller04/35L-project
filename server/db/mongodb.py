from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
MONGO_DETAILS = MONGO_URI

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

async_client = AsyncIOMotorClient(MONGO_DETAILS)
async_db = async_client[DATABASE_NAME]
users_collection = async_db.get_collection("users")
course_collection = async_db.get_collection("courses")
valid_course_collection = async_db.get_collection("valid_courses")
ratings_collection = async_db.get_collection("course_ratings")
descriptions_collection = async_db.get_collection("descriptions")
professor_ratings_collection = async_db.get_collection("professor_ratings")

pre_reqs = async_db.get_collection("pre-reqs")
previous_courses = async_db.get_collection("Previous courses")
future_courses = async_db.get_collection("Future courses")
sample = async_db.get_collection("sample")
aliases = async_db.get_collection("Aliases")


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