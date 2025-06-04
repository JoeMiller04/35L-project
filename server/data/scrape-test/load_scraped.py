import os
from pymongo import MongoClient
import json
from pathlib import Path

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "35L-project")


def parse_time_to_schedule(days_str, time_str):
    """
    Parse the days string and time string into a proper format
    
    Example:
    days_str = "MW"
    time_str = "10:00 am - 11:50 am"
    
    Result:
    {
        "M": [1000, 1150],
        "W": [1000, 1150]
    }
    """
    if not days_str or not time_str:
        return None
    
    if "Varies" in days_str or "Varries" in time_str:
        return None

    if "Not scheduled" in days_str or "Not scheduled" in time_str:
        return None
    
    # Create a dictionary for the schedule
    schedule = {}
    
    # Map day characters to their full names
    days_map = {
        'M': 'Monday',
        'T': 'Tuesday',
        'W': 'Wednesday',
        'R': 'Thursday', 
        'F': 'Friday'
    }
    
    
    # Parse the time string
    # It usually looks like "TR\n        \n        2pm-3:50pm"
    try:
        # Take everything after the last space
        time_str = time_str.split()[-1]
        # Split the time range
        time_range = time_str.split('-')
        if len(time_range) != 2:
            print(f"Invalid time range format: {time_str}")
            return None

        # Parse start and end times
        start_time_str = time_range[0].strip()
        end_time_str = time_range[1].strip()
        if "am" not in start_time_str and "pm" not in start_time_str:
            print(f"Invalid start time format: {start_time_str}")
            return None
        if "am" not in end_time_str and "pm" not in end_time_str:
            print(f"Invalid end time format: {end_time_str}")
            return None

        # Save in military time format
        start_res = 0
        end_res = 0

        if ":" in start_time_str:
            start_res = int(start_time_str.replace(":", "").replace("am", "").replace("pm", ""))
        else:
            start_res = int(start_time_str.replace("am", "").replace("pm", ""))
            start_res *= 100
        if "pm" in start_time_str and start_res < 1200:
            start_res += 1200
        if ":" in end_time_str:
            end_res = int(end_time_str.replace(":", "").replace("am", "").replace("pm", ""))
        else:
            end_res = int(end_time_str.replace("am", "").replace("pm", ""))
            end_res *= 100
        if "pm" in end_time_str and end_res < 1200:
            end_res += 1200
        
        schedule = {days_map[day]: [start_res, end_res] for day in days_str if day in days_map}

        return schedule


    
    except Exception as e:
        print(f"Error parsing time schedule: {e}")
        return None
    
    return schedule



def upload(courses):
    """
    Upload courses to MongoDB, checking for duplicates
    """
    # Get the courses collection
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db["courses"]
    
    # Keeping Track
    added_count = 0
    skipped_count = 0
    updated_count = 0

    for course_data in courses:
        # Skip if missing essential fields
        if not all(k in course_data for k in ['subject', 'instructor', 'title', 'term']):
            print(f"Skipping incomplete course: {course_data}")
            skipped_count += 1
            continue
        
        # Clean up the data for MongoDB
        clean_course = {
            'real': True,  # This is a real course from the schedule
            'term': course_data['term'],
            'subject': course_data['subject'],
            'instructor': course_data['instructor'],
        }

        # catalog_cleaned is wrong, so we can't use that
        # The title is actually: [catalog number] - [title]
        # Extract catalog and title from the title field
        title_parts = course_data['title'].split(' - ', 1)
        if len(title_parts) == 2:
            clean_course['catalog'] = title_parts[0].strip()
            clean_course['title'] = title_parts[1].strip()
        else:
            print(f"Skipping course with strange title: {course_data['title']}")
            skipped_count += 1
            continue
        
        # Parse days and time into a schedule if available
        if 'days' in course_data and 'time' in course_data:
            clean_course['times'] = parse_time_to_schedule(course_data['days'], course_data['time'])
        
        # Add location if available
        if 'location' in course_data:
            clean_course['location'] = course_data['location']
        
        # Check if this course already exists
        existing_course = collection.find_one({
            'term': clean_course['term'],
            'subject': clean_course['subject'],
            'catalog': clean_course['catalog'],
            'instructor': clean_course['instructor']
        })
        
        if existing_course:
            # print(f"Skipping duplicate course: {clean_course['subject']} {clean_course['catalog']} - {clean_course['instructor']}")
            # If existing course found, if it doesn't have a times, update it
            if 'times' not in existing_course and 'times' in clean_course and clean_course['times']:
                # Update the existing course with the time information
                update_result = collection.update_one(
                    {'_id': existing_course['_id']},
                    {'$set': {'times': clean_course['times']}}
                )
                print(f"Updated course with time information: {clean_course['subject']} {clean_course['catalog']} - {clean_course['instructor']}")
                print(f"Update result: matched={update_result.matched_count}, modified={update_result.modified_count}")
                updated_count += update_result.modified_count
            else:
                skipped_count += 1   
        else:
            # Insert the new course
            result = collection.insert_one(clean_course)
            print(f"Added course: {clean_course['subject']} {clean_course['catalog']} - {clean_course['instructor']} (ID: {result.inserted_id})")
            added_count += 1
    
    print(f"MongoDB upload complete: {added_count} courses added, {skipped_count} duplicates skipped, {updated_count} courses updated")
    return added_count, skipped_count, updated_count


def main():
    data_dir = Path("course_data")
    
    for json_file in sorted(data_dir.glob("*.json")):
        print(f"Processing file: {json_file}")
        
        with open(json_file, 'r') as f:
            courses = json.load(f)
        
        # # Upload courses to MongoDB
        added_count, skipped_count, updated_count = upload(courses)
        
        print(f"File {json_file} processed: {added_count} added, {skipped_count} skipped, {updated_count} updated")


if __name__ == "__main__":
    main()

