"""
Script to load course descriptions from a JSON file into MongoDB.

Usage:
    python load_descriptions.py <json_file_path>
"""

import json
import sys
import os
import argparse
from pymongo import MongoClient, ASCENDING
from bson import json_util
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")


def load_descriptions(json_file_path, db, drop_existing=False):
    """
    Load course descriptions from a JSON file into MongoDB
    Returns:
        Tuple of (total_courses, added_courses)
    """
    if not MONGO_URI or not DATABASE_NAME:
        print("MONGO_URI or DATABASE_NAME is not set in the environment variables.")
        return None, None
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db["descriptions"]
    
    # Create index on subject and catalog for faster lookups
    collection.create_index([("subject", ASCENDING), ("catalog", ASCENDING)], unique=True)
    
    # Drop the collection if requested
    if drop_existing:
        print("Dropping existing 'descriptions' collection...")
        collection.drop()
    
    # Load the JSON file
    print(f"Loading descriptions from {json_file_path}...")
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"Found {len(data)} course descriptions in the file.")
    
    # Counter for added courses
    added_count = 0
    skipped_count = 0
    error_count = 0
    
    # Import each course description
    for course in data:
        try:
            # Remove the MongoDB ObjectId if present
            if "_id" in course:
                del course["_id"]
            
            # Check if a course with this subject and catalog already exists
            existing_course = collection.find_one({
                "subject": course["subject"],
                "catalog": course["catalog"]
            })
            
            if existing_course:
                skipped_count += 1
                continue
            
            result = collection.insert_one(course)
            added_count += 1

            if added_count % 1000 == 0:
                print(f"Added {added_count} courses so far...")
            
        
        except Exception as e:
            print(f"Error importing course {course.get('subject', 'Unknown')} {course.get('catalog', 'Unknown')}: {e}")
            error_count += 1
    
    print(f"\nImport complete!")
    print(f"Total courses in file: {len(data)}")
    print(f"Courses added: {added_count}")
    print(f"Courses skipped (already exist): {skipped_count}")
    print(f"Errors: {error_count}")
    
    return len(data), added_count

def main():
    """Main function to handle command line arguments and execute the import"""
    parser = argparse.ArgumentParser(description='Import course descriptions from JSON to MongoDB')
    parser.add_argument('file_path', help='Path to the JSON file containing course descriptions')
    parser.add_argument('--drop', action='store_true', help='Drop existing collection before import')
    
    args = parser.parse_args()
    
    # Check if the file exists
    if not os.path.exists(args.file_path):
        print(f"Error: File not found: {args.file_path}")
        return 1
    
    try:
        # Load the descriptions
        if not MONGO_URI or not DATABASE_NAME:
            print("MONGO_URI or DATABASE_NAME is not set in the environment variables.")
            return
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db["descriptions"]
        total, added = load_descriptions(args.file_path, db, args.drop)
        
        # Close connection
        client.close()
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())