#!/usr/bin/env python3

import sys
import os
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from server.db.mongodb import pre_reqs as reqs
from server.db.mongodb import previous_courses as pc
from server.db.mongodb import future_courses as fc
from server.db.mongodb import sample as sp
from server.db.mongodb import aliases as ali
from server.db.mongodb import users_collection as users

from bson.objectid import ObjectId

quarter_order = {"w": 0, "s": 1, "1": 2, "f": 3}

def parse_catalog_year(catalog_year):
    # Example input: "21f"
    if len(catalog_year) != 3:
        return None  # or raise error
    year = int(catalog_year[:2])
    quarter = catalog_year[2].lower()
    if quarter not in quarter_order:
        return None
    return (year, quarter_order[quarter])

def find_lowest_quarter(other_courses):
    parsed = [parse_catalog_year(c.get("term", "")) for c in other_courses]
    parsed = [p for p in parsed if p is not None]
    if not parsed:
        return None
    return min(parsed)  # tuple comparison works (year, quarter_order)

def generate_quarter_sequence(start_year, start_quarter_idx, num_years=4):
    # Generate catalog_year strings from start point, covering num_years ahead
    
    quarters = ["W", "S", "SS", "F"]
    sequence = []
    year = start_year
    quarter_idx = start_quarter_idx
    
    for _ in range(num_years * 4):  # 3 quarters per year
        catalog_str = f"{year:02d}{quarters[quarter_idx]}"
        sequence.append(catalog_str)
        
        quarter_idx += 1
        if quarter_idx >= 3:
            quarter_idx = 0
            year += 1
    return sequence

async def isValid(previous_courses, sorted_list, eng_comp):
    taken_courses = []
    for course in previous_courses:
        taken_courses.append(course["course_name"])
    GE_counter = 0
    SCI_TECH_counter = 0
    TECH_BREADTH_counter = 0
    eng_comp_bool = eng_comp
    total_units = 0
    ethics_requirement = False
    elective_counter = 0 # elective that are given with the placeholder name "COM SCI ELECTIVE"
    specified_elective_counter = 0 #electives that have been explicitly stated
    quarter_tester = ""
    quarter_courses = []

    for course_name in taken_courses:
        if course_name in ("GE 1", "GE 2", "GE 3", "GE 4", "GE 5"):
            GE_counter += 1
            total_units += 5
        elif course_name in ("SCI TECH 1", "SCI TECH 2", "SCI TECH 3"):
            SCI_TECH_counter += 1
            total_units += 4
        elif course_name in ("TECH BREADTH 1", "TECH BREADTH 2", "TECH BREADTH 3"):
            TECH_BREADTH_counter += 1
            total_units += 4
        elif course_name == "ENGCOMP 3":
            eng_comp_bool = True
            total_units += 4
        elif course_name == "ETHICS":
            ethics_requirement = True
            total_units +=4
        elif course_name == "COM SCI ELECTIVE":
            elective_counter += 1
            total_units += 4
        else:
            result = await reqs.find_one({"course_name": course_name})
            if not result:
                alias_result = ali.find_one({"alias_key": course_name})
                if alias_result:
                    course_name = alias_result.get("original_course")
                    result = await reqs.find_one({"course_name": course_name})
                else:
                    raise ValueError(f"Invalid course entry: {course_name}")

            elective_true = result.get("elective_eligible")  
            if elective_true:
                specified_elective_counter += 1
            
            # Add units
            units = result.get("units")
            if units is not None:
                total_units += units

            # Check pre-reqs
            requisite_courses = result.get("requisites", [])
            for group in requisite_courses:  # group is a list of course names
                if not any(pre_req in taken_courses for pre_req in group):
                    raise ValueError(f"Pre-requisite '{group}' for {course_name} not met") 

    for course in sorted_list:
        course_name = course.get('course_name', '').strip()
        course_quarter = course.get('term').strip()
        if quarter_tester != course_quarter:
            quarter_tester = course_quarter
            for a in quarter_courses:
                taken_courses.append(a) # add all previous quarter courses to taken courses
            quarter_courses = []
            quarter_courses.append(course)
        else:
            quarter_courses.append(course)
        if course_name == "GE":
            GE_counter += 1
            total_units += 5
        elif course_name == "SCI-TECH":
            SCI_TECH_counter += 1
            total_units += 4
        elif course_name == "TECH BREADTH":
            TECH_BREADTH_counter += 1
            total_units += 4
        elif course_name == "ENG COMP":
            eng_comp_bool = True
            total_units += 4
        elif course_name == "ETHICS":
            ethics_requirement = True
            total_units +=4
        elif course_name == "COM SCI ELECTIVE":
            elective_counter += 1
            total_units += 4
        else:
            result = await reqs.find_one({"course_name": course_name})
            if not result:
                alias_result = ali.find_one({"alias_key": course_name})
                if alias_result:
                    course_name = alias_result.get("original_course")
                    result = await reqs.find_one({"course_name": course_name})
                else:
                    raise ValueError(f"Invalid course entry: {course_name}")

            elective_true = result.get("elective_eligible")  
            if elective_true:
                specified_elective_counter += 1
            
            # Add units
            units = result.get("units")
            if units is not None:
                total_units += units

            # Check pre-reqs
            requisite_courses = result.get("requisites", [])
            for group in requisite_courses:  # group is a list of course names
                if not any(pre_req in taken_courses for pre_req in group):
                    raise ValueError(f"Pre-requisite '{group}' for {course_name} not met")    

    #Lower-div courses
    for element in ["PHYSICS 1A", "PHYSICS 1B", "PHYSICS 1C"]:
        if not any(course.strip().upper() == element for course in taken_courses):
            raise ValueError(f"Lower division physics requirement not met. {element} not taken.")
    if "PHYSICS 4AL" not in taken_courses and "PHYSICS 4BL" not in taken_courses:
        raise ValueError (f"Lower division physics requirements not met. You must take either Physics 4AL or 4BL.")
    for element in ["MATH 31A", "MATH 31B", "MATH 32A", "MATH 32B", "MATH 33A", "MATH 33B"]:
        if not any(course.strip().upper() == element for course in taken_courses):
            raise ValueError (f"Lower division math requirements not met. {element} not taken.")
    for element in ["COM SCI 31", "COM SCI 32", "COM SCI 33", "COM SCI 35L", "COM SCI M51A"]:
        if not any(course.strip().upper() == element for course in taken_courses):
            raise ValueError (f"Lower division computer science requirements not met. {element} not taken.")
    
    #Upper div checks
    if "COM SCI 130" not in taken_courses and "COM SCI 132" not in taken_courses:
        raise ValueError(f"Upper division computer science requirements not met. You must take either COM SCI 130 or COM SCI 132.")
    for element in ["COM SCI 111", "COM SCI 118", "COM SCI 131", "COM SCI M151B", "COM SCI M152A",
                    "COM SCI 180", "COM SCI 181"]:
        if not any(course.strip().upper() == element for course in taken_courses):
            raise ValueError(f"Upper division computer science requirements not met. {element} not taken.")
    if "COM SCI 130" not in taken_courses and "COM SCI 152B" not in taken_courses:
        raise ValueError(f"Upper division computer science requirements not met. You must take either COM SCI 130 or COM SCI 152B.")
    if "COM SCI 130" in taken_courses and "COM SCI 152B" in taken_courses: #both taken, one as an elective, one as a requirement
        specified_elective_counter -= 1
    if ("COM SCI 130" in taken_courses) ^ ("COM SCI 152B" in taken_courses): #xor one taken, only as a requirement
        specified_elective_counter -= 1
    if "MATH 170A" in taken_courses and "MATH 170E" in taken_courses: #probability requirement
        raise ValueError(f"Upper division probability requirement not met. You must take MATH 170A, 170E or any of its equivalents.")

    #elective checker
    if (elective_counter + specified_elective_counter) < 5:
        raise ValueError(f"Upper division computer science requirements not met. You must take at least 5 upper-divison electives.")

    #Other requirements
    if not ethics_requirement:
        raise ValueError(f"Ethics Requirement Not Met")
    if GE_counter < 5:
        raise ValueError(f"Not enoguh GEs")
    if SCI_TECH_counter < 3:
        raise ValueError(f"Not enoguh SCI-TECH courses")
    if TECH_BREADTH_counter < 3:
        raise ValueError(f"Not enoguh TECH BREADTH courses")
    if total_units < 180:
        raise ValueError(f"Lower than 180 total units")
    if not eng_comp_bool:
        raise ValueError(f"English composition requirement not satisfied")
    
    return True

async def upload_courses(user_id):
    user_doc = await users.find_one({"_id": ObjectId(user_id)})
    if user_doc and "saved_courses" in user_doc:
        past_courses = []
        other_courses = []

        for course in user_doc["saved_courses"]:
            course_name = course["course_name"]
            term = course["term"]
            course_dict = {"course_name": course_name, "term": term}

            if term == "PAST":
                past_courses.append(course_dict)
            else:
                other_courses.append(course_dict)

        return past_courses, other_courses
    else:
        raise ValueError("User not found or no saved_courses")

    
async def executioner(user_id, eng_comp: bool = False):
    other_courses = []

    already_taken, other_courses = await upload_courses(user_id)  

    '''this didn't work bc of GE, TECH BREADTH and SCI-TECH duplicates
    if duplicates:
        print(f"Found {len(duplicates)} duplicate(s) based on course_name:")
        for dup in duplicates:
            print(f"- Duplicate: {dup.get('course_name')} ({dup.get('catalog_year')})")
    '''

    #print(f"Total courses: {len(other_courses) + len(already_taken)}")
    
    lowest = find_lowest_quarter(other_courses)
    if not lowest and already_taken == []:
        return other_courses, False  # no sorting if no valid quarters found
    start_year, start_quarter_idx = lowest
    quarter_sequence = generate_quarter_sequence(start_year, start_quarter_idx)    
    priority_map = {q: i for i, q in enumerate(quarter_sequence)}
    other_courses.sort(key=lambda c: priority_map.get(c.get("term", ""), 9999))

    validity = await isValid(already_taken, other_courses, eng_comp)

    return other_courses, validity


async def main():
    other_courses, validity = await executioner('6840d18240100a7eb9ebc999')
    if validity:
        print("The list satisfies CS requirements")
    else:
        print("The list is invalid")
    '''
    for item in other_courses:
        print(item.get('course_name'), item.get('term'))
    '''

if __name__ == "__main__":
    asyncio.run(main())
