#!/usr/bin/env python3

from pymongo import MongoClient
import os

def sample():
    course_list = [
        {"Course": "COM SCI 1", "Quarter": "20F"},
        {"Course": "COM SCI 31", "Quarter": "20F"},
        {"Course": "ENG COMP", "Quarter": "20F"},
        {"Course": "MATH 31A", "Quarter": "20F"},
        
        {"Course": "COM SCI 32", "Quarter": "21W"},
        {"Course": "MATH 31B", "Quarter": "21W"},
        {"Course": "PHYSICS 1A", "Quarter": "21W"},
        
        {"Course": "COM SCI 33", "Quarter": "21S"},
        {"Course": "MATH 32A", "Quarter": "21S"},
        {"Course": "PHYSICS 1B", "Quarter": "21S"},

        {"Course": "COM SCI 35L", "Quarter": "21F"},
        {"Course": "COM SCI M51A", "Quarter": "21F"},
        {"Course": "MATH 32B", "Quarter": "21F"},
        {"Course": "ETHICS", "Quarter": "21F"},

        {"Course": "MATH 33A", "Quarter": "22W"},
        {"Course": "MATH 61", "Quarter": "22W"},
        {"Course": "PHYSICS 1C", "Quarter": "22W"},
        {"Course": "PHYSICS 4AL", "Quarter": "22W"},

        {"Course": "COM SCI 111", "Quarter": "22S"},
        {"Course": "COM SCI M152A", "Quarter": "22S"},
        {"Course": "MATH 33B", "Quarter": "22S"},
        {"Course": "GE", "Quarter": "22S"},

        {"Course": "COM SCI 118", "Quarter": "22F"},
        {"Course": "COM SCI 180", "Quarter": "22F"},
        {"Course": "SCI-TECH", "Quarter": "22F"},
        {"Course": "GE", "Quarter": "22F"},

        {"Course": "COM SCI 131", "Quarter": "23W"},
        {"Course": "COM SCI M151B", "Quarter": "23W"},
        {"Course": "MATH 170A", "Quarter": "23W"},
        {"Course": "GE", "Quarter": "23W"},

        {"Course": "COM SCI 181", "Quarter": "23S"},
        {"Course": "COM SCI 112", "Quarter": "23S"},
        {"Course": "TECH BREADTH", "Quarter": "23S"},
        {"Course": "GE", "Quarter": "23S"},

        {"Course": "COM SCI 130", "Quarter": "23F"},
        {"Course": "COM SCI C121", "Quarter": "23F"},
        {"Course": "SCI-TECH", "Quarter": "23F"},
        {"Course": "GE", "Quarter": "23F"},

        {"Course": "COM SCI 132", "Quarter": "24W"},
        {"Course": "COM SCI 134", "Quarter": "24W"},
        {"Course": "COM SCI C137A", "Quarter": "24W"},
        {"Course": "TECH BREADTH", "Quarter": "24W"},

        {"Course": "COM SCI 161", "Quarter": "24S"},
        {"Course": "SCI-TECH", "Quarter": "24S"},
        {"Course": "TECH BREADTH", "Quarter": "24S"}
    ]
    return course_list
    
def upload_to_mongodb(course_list):
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "35L-project")

    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db["sample"]
    result = collection.insert_many(course_list)
    print(f"Inserted {len(result.inserted_ids)} documents.")

if __name__ == "__main__":
    sample = sample()
    upload_to_mongodb(sample)