#!/usr/bin/env python3

from pymongo import MongoClient
from collections import defaultdict
import re

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

def export_to_mongodb():
    with open("more_reviews.txt", "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.count(":") < 2:
                continue  # skip empty or malformed lines
            course, prof, rating = [part.strip() for part in line.split(":", 2)]
            course_map[course].append({"name": prof, "rating": rating})

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

if __name__ == "__main__":
    print("Exporting data to MongoDB...")
    count = export_to_mongodb()