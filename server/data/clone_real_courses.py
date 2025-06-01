"""
This script:
1. Pulls existing courses from MongoDB for specific subjects
2. Creates clones of these courses with:
   - term set to "25S"
   - real set to False
   - Added time slots
"""

import random
from pymongo import MongoClient
import os
from datetime import datetime
import copy

# MongoDB connection details
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "35L-project")

# Subjects we want to clone
SUBJECTS = ["COM SCI", "EC ENGR", "MATH", "PHYSICS"]

# Possible days for classes
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Time slots (24-hour format)
TIME_SLOTS = [
    # Morning classes
    (800, 850),   # 8:00 - 8:50 AM
    (900, 950),   # 9:00 - 9:50 AM
    (1000, 1050), # 10:00 - 10:50 AM
    (1100, 1150), # 11:00 - 11:50 AM
    
    # Afternoon classes
    (1200, 1250), # 12:00 - 12:50 PM
    (1300, 1350), # 1:00 - 1:50 PM
    (1400, 1450), # 2:00 - 2:50 PM
    (1500, 1550), # 3:00 - 3:50 PM
    (1600, 1650), # 4:00 - 4:50 PM
    
    # Evening classes
    (1700, 1750), # 5:00 - 5:50 PM
    
    # Longer classes
    (900, 1050),  # 9:00 - 10:50 AM
    (1100, 1250), # 11:00 - 12:50 PM
    (1400, 1550), # 2:00 - 3:50 PM
    (1600, 1750)  # 4:00 - 5:50 PM
]

# Function to generate time schedules
def generate_time_schedule():
    """Generate a realistic time schedule for a course"""
    num_days = random.choice([1, 2, 3])  # Most classes meet 1-3 days per week
    chosen_days = random.sample(DAYS, num_days)
    time_slot = random.choice(TIME_SLOTS)
    
    # Create time schedule dictionary
    schedule = {}
    
    # Use the same time for all days
    for day in chosen_days:
        schedule[day] = time_slot
    
    return schedule

def clone_real_courses():
    """Clone existing courses with new term and time information"""
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db["courses"]
        
        # Find all courses with the target subjects and real=True
        query = {
            "subject": {"$in": SUBJECTS},
            "real": True
        }
        
        # Get all matching courses
        original_courses = list(collection.find(query))
        print(f"Found {len(original_courses)} original courses")
        
        # Create clones with modifications
        cloned_courses = []
        
        for course in original_courses:
            # Create a deep copy to avoid modifying the original
            cloned_course = copy.deepcopy(course)
            
            # Remove the MongoDB _id field so a new one will be generated
            if "_id" in cloned_course:
                del cloned_course["_id"]
            
            # Update the fields
            cloned_course["real"] = False
            cloned_course["term"] = "25S"
            cloned_course["times"] = generate_time_schedule()
            cloned_course["import_date"] = datetime.now()
            
            cloned_courses.append(cloned_course)
        
        # Insert all cloned courses
        if cloned_courses:
            result = collection.insert_many(cloned_courses)
            print(f"Successfully cloned and inserted {len(result.inserted_ids)} courses")
            return len(result.inserted_ids)
        
        return 0
        
    except Exception as e:
        print(f"Error cloning courses: {str(e)}")
        return 0

if __name__ == "__main__":
    print("Cloning existing courses with new term and time information...")
    count = clone_real_courses()
    print(f"Created {count} cloned courses for term 25S with time information")