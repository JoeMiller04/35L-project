#!/usr/bin/env python3
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

MONGO_URI = "mongodb://localhost:27017"

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "35L-project")
MONGO_DETAILS = "mongodb://localhost:27017" 

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
course_ratings = db.get_collection("course_ratings")

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def fetch_and_print_overall_rating(input_url : str, page_number : int):
    url = f"{input_url}{page_number}"
    #print(f"Requesting URL: {url}\n")

    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f'Cannot connect to this page{url}')
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    results = []

    class_cards = soup.find_all('div', class_='top-text')

    for card in class_cards:
        # Extract professor name
        professor_tag = card.find('a')
        professor_name = professor_tag.text.strip() if professor_tag else "Unknown"

        # Extract overall rating
        rating_tag = card.find('b', class_='overall-rating-badge')
        overall_rating = rating_tag.text.strip() if rating_tag else "N/A"

        results.append({
            "professor": professor_name,
            "rating": overall_rating
        })

    return results

def get_all_course_names():
    cursor = course_ratings.find({}, {"subject": 1, "catalog": 1, "_id": 0})
    return [f"{doc['subject'].lower()}-{doc['catalog'].lower()}" for doc in cursor]


def save_professor_reviews():    
    all_class_scores = []
    seen = set()  # Track (course, professor) pairs to avoid duplicates
    collection = get_all_course_names()

    for original_name in collection:

        url = f"https://www.bruinwalk.com/classes/{original_name}/?page="

        for page in range(1, 11):
            class_scores = fetch_and_print_overall_rating(url, page)
            if class_scores:
                for entry in class_scores:
                    course_name = original_name
                    professor_name = entry["professor"]

                    # Use tuple key to track duplicates
                    key = (course_name, professor_name)
                    if key not in seen:
                        seen.add(key)
                        entry["course"] = course_name
                        all_class_scores.append(entry)
            time.sleep(1)  # Avoid hammering server

    for course in all_class_scores:
        print(f"{course['course']}: {course['professor']}: {course['rating']}")


if __name__ == '__main__':
    save_professor_reviews()