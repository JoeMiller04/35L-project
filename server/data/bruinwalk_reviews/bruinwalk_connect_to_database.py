#!/usr/bin/env python3

from pymongo import MongoClient
import os


def export_to_mongodb():

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "35L-project")

    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db["course_ratings"]

    try:
        with open("results.txt", "r") as file:
            for line in file:
                if ":" in line:
                    course, rating = line.strip().split(":")
                    course = course.strip()
                    rating = float(rating.strip())

                    document = {
                        "course": course,
                        "rating": rating
                    }
                    collection.insert_one(document)

    except Exception as e:
        print(f"Error exporting to MongoDB: {e}")
        return 0


if __name__ == "__main__":
    print("Exporting data to MongoDB...")
    count = export_to_mongodb()