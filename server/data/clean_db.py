from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "35L-project")


def clean_db():
    """
    Clean the database by removing all courses that are not real.
    """
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
    