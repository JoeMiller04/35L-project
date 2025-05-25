#!/usr/bin/env python3

from pymongo import MongoClient
import os

"""
results.txt format:
Every line should be in the format: 
[subject] [catalog number]: [rating]
E.g. "COM SCI 35L: 4.5"
"""


def export_to_mongodb():

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "35L-project")

    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db["course_ratings"]

    count = 0

    try:
        with open("results.txt", "r") as file:
            for line in file:
                if ":" in line:
                    course, rating = line.strip().split(":")
                    course = course.strip()
                    rating = float(rating.strip())

                    course_parts = course.split(" ")
                    catalog = course_parts[-1]
                    subject = " ".join(course_parts[:-1])

                    document = {
                        "subject": subject,
                        "catalog": catalog,
                        "rating": rating
                    }
                    collection.insert_one(document)
                    count += 1

    except Exception as e:
        print(f"Error exporting to MongoDB: {e}")
        return 0


if __name__ == "__main__":
    print("Exporting data to MongoDB...")
    count = export_to_mongodb()
    print(f"Exported {count} records to MongoDB.")