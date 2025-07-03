from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")


def clean_db():
    """
    Clean the database by removing all courses that are not real.
    """
    if not MONGO_URI or not DATABASE_NAME:
        print("MONGO_URI or DATABASE_NAME is not set in the environment variables.")
        return

    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db["courses"]
    
    # Remove all courses where 'real' is False
    result = collection.delete_many({"real": False})

    print(f"Removed {result.deleted_count} non-real courses from the database.")
    
    client.close()


if __name__ == "__main__":
    print("Cleaning the database of non-real courses...")
    clean_db()
    