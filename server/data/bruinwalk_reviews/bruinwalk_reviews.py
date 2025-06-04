#!/usr/bin/env python3

import requests
import time
from bs4 import BeautifulSoup
import re
from decimal import Decimal

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def fetch_and_print_overall_rating(input_url : str, page_number : int):
    url = f"{input_url}{page_number}"
    #print(f"Requesting URL: {url}\n")

    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Failed to load page: Status code {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    results = []

    class_cards = soup.find_all('div', class_='flex-container class-meta-content')

    for card in class_cards:
        # Get class name
        class_name_tag = card.find('div', class_='class-id')
        class_name = class_name_tag.text.strip() if class_name_tag else "Unknown"

        # Get overall rating
        rating_tag = card.find('b', class_='rating')
        rating = rating_tag.text.strip() if rating_tag else "N/A"

        results.append((class_name, rating))

    return results

def executioner():
    all_class_scores = []
    min_rating = Decimal("1.0")
    max_rating = Decimal("4.9")
    step = Decimal("0.1")

    for rating in [min_rating + i * step for i in range(int((max_rating - min_rating) / step) + 1)]:
        rating_str = str(rating)

        url = (
            f"https://www.bruinwalk.com/search/?category=classes"
            f"&dept=-1"
            f"&min={rating_str}&max={rating_str}"
            f"&min-price=500&max-price=10000"
            f"&min_baths=0&max_baths=5"
            f"&min_beds=0&max_beds=5"
            f"&sort=overall"
            f"&page="
        )
        for page in range(1, 101):  # Adjust page range as needed
            class_scores = fetch_and_print_overall_rating(url, page)
            all_class_scores.extend(class_scores)
            time.sleep(1)

    for cls, rating in all_class_scores:
        print(f"{cls}: {rating}")

if __name__ == '__main__':
    executioner()