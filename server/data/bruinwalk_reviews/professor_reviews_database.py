#!/usr/bin/env python3

from pymongo import MongoClient
from collections import defaultdict

MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["35L-project"]
prof_ratings = db["professor-ratings"]

course_map = defaultdict(list)

def professor_reviews():
    with open("professor_reviews.txt", "r") as file:
        for line in file:
            line = line.strip()
            course, prof, rating = [part.strip() for part in line.split(":", 2)]
            course_map[course].append({"name": prof, "rating": rating})

    for course_name, professors in course_map.items():
        data = {
            "course_name": course_name,
            "professors": professors
        }
        prof_ratings.update_one(
            {"course_name": course_name},
            {"$set": data},
            upsert=True
        )

print("Upload complete.")