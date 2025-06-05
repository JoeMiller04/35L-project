#!/usr/bin/env python3

from pymongo import MongoClient
import os
import argparse

"""
results.txt format:
Every line should be in the format: 
[subject] [catalog number]: [rating]
E.g. "COM SCI 35L: 4.5"
Running mulitple times will append to the existing data.
"""


def export_to_mongodb(filename="results.txt"):

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "35L-project")

    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db["course_ratings"]

    print("Dropping existing 'course_ratings' collection...")
    collection.drop()

    count = 0

    try:
        with open(filename, "r") as file:
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
        return count
    except Exception as e:
        print(f"Error exporting to MongoDB: {e}")
        return 0


def main():
    parser = argparse.ArgumentParser(description='Import course reviews from txt to MongoDB')
    parser.add_argument('file_path', help='Path to the txt file containing course reviews')
    args = parser.parse_args()
    print("Exporting data to MongoDB...")
    count = export_to_mongodb(args.file_path)
    print(f"Exported {count} records to MongoDB.")

if __name__ == "__main__":
    main()