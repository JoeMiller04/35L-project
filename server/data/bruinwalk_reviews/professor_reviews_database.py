#!/usr/bin/env python3

from pymongo import MongoClient
from collections import defaultdict
import re
import argparse

MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["35L-project"]
prof_ratings = db["professor_ratings"]

course_map = defaultdict(list)

def split_course_name(full_name):
    #"COM SCI 1" -> ("COM SCI", "1"), "COM SCI M152A" -> ("COM SCI", "M152A")
    match = re.match(r"([A-Z\s]+)\s+([A-Z]*\d+[A-Z]*)$", full_name.strip(), re.IGNORECASE)
    if match:
        dept, number = match.groups()
        return dept.strip().upper(), number.upper()
    else:
        return full_name.strip().upper(), ""  

def export_to_mongodb(filename="professor_reviews.txt"):
    count = 0
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            course, prof, rating = [part.strip() for part in line.split(":", 2)]
            course_map[course].append({"name": prof, "rating": rating})
            count += 1

    for full_course_name, professors in course_map.items():
        subject, catalog = split_course_name(full_course_name)
        data = {
            "subject": subject,
            "catalog": catalog,
            "professors": professors
        }
        prof_ratings.update_one(
            {"subject": subject, "catalog": catalog},
            {"$set": data},
            upsert=True
        )
    print("Upload complete.")
    return count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Import professor reviews from txt file to MongoDB')
    parser.add_argument('file_path', help='Path to the txt file containing professor reviews')
    args = parser.parse_args()
    print("Exporting data to MongoDB...")
    count = export_to_mongodb(args.file_path)
    print(f"Uploaded {count} course+professor ratings.")