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
import server.db.mongodb as mongod

quarter_order = {"w": 0, "s": 1, "f": 2}

def parse_catalog_year(catalog_year):
    # Example input: "21f"
    if len(catalog_year) != 3:
        return None  # or raise error
    year = int(catalog_year[:2])
    quarter = catalog_year[2].lower()
    if quarter not in quarter_order:
        return None
    return (year, quarter_order[quarter])

def find_lowest_quarter(local_list):
    parsed = [parse_catalog_year(c.get("Quarter", "")) for c in local_list]
    parsed = [p for p in parsed if p is not None]
    if not parsed:
        return None
    return min(parsed)  # tuple comparison works (year, quarter_order)

def generate_quarter_sequence(start_year, start_quarter_idx, num_years=5):
    # Generate catalog_year strings from start point, covering num_years ahead
    
    quarters = ["W", "S", "F"]
    sequence = []
    year = start_year
    quarter_idx = start_quarter_idx
    
    for _ in range(num_years * 3):  # 3 quarters per year
        catalog_str = f"{year:02d}{quarters[quarter_idx]}"
        sequence.append(catalog_str)
        
        quarter_idx += 1
        if quarter_idx >= 3:
            quarter_idx = 0
            year += 1
    return sequence

async def upload_previous_courses():
    
    cursor = sp.find()
    return [doc async for doc in cursor]
    

async def upload_future_courses():
    ''' 
    return mongod.list_documents("sample")
    '''
    return []

async def isValid(previous_courses, sorted_list, eng_comp):
    taken_courses = []
    for course in previous_courses:
        taken_courses.append(course)
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

    for course in sorted_list:
        course_name = course.get('Course', '').strip()
        course_quarter = course.get('Quarter').strip()
        if quarter_tester != course_quarter:
            quarter_tester = course_quarter
            for a in quarter_courses:
                taken_courses.append(a) # add all previous quarter courses to taken courses
            quarter_courses = []
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
            
            quarter_courses.append(course_name) #temp add to quarter

    #Lower-div courses
    for element in ["PHYSICS 1A", "PHYSICS 1B", "PHYSICS 1C"]:
        if not any(
        isinstance(course, dict) and course.get("Course", "").strip().upper() == element
        for course in taken_courses
        ):
            raise ValueError(f"Lower division physics requirement not met. {element} not taken.")
    if not any(
        isinstance(course, dict) and course.get("Course", "").strip().upper() == "PHYSICS 4AL" for course in taken_courses)\
        and not any(isinstance(course, dict) and course.get("Course", "").strip().upper() == "PHYSICS 4BL"
        for course in taken_courses
        ):
            raise ValueError (f"Lower division physics requirements not met. You must take either Physics 4AL or 4BL.")
    for element in ["MATH 31A", "MATH 31B", "MATH 32A", "MATH 32B", "MATH 33A", "MATH 33B"]:
        if not any(
        isinstance(course, dict) and course.get("Course", "").strip().upper() == element
        for course in taken_courses
        ):
            raise ValueError (f"Lower division math requirements not met. {element} not taken.")
    for element in ["COM SCI 31", "COM SCI 32", "COM SCI 33", "COM SCI 35L", "COM SCI M51A"]:
        if not any(
        isinstance(course, dict) and course.get("Course", "").strip().upper() == element
        for course in taken_courses
        ):
            raise ValueError (f"Lower division computer science requirements not met. {element} not taken.")
    
    #Upper div checks
    if not any(
        isinstance(course, dict) and course.get("Course", "").strip().upper() == "COM SCI 130" for course in taken_courses)\
        and not any(isinstance(course, dict) and course.get("Course", "").strip().upper() == "COM SCI 132"
        for course in taken_courses
        ):
            raise ValueError(f"Upper division computer science requirements not met. You must take either COM SCI 130 or COM SCI 132.")
    for element in ["COM SCI 111", "COM SCI 118", "COM SCI 131", "COM SCI M151B", "COM SCI M152A",
                    "COM SCI 180", "COM SCI 181"]:
        if not any(
        isinstance(course, dict) and course.get("Course", "").strip().upper() == element
        for course in taken_courses
        ):
            raise ValueError(f"Upper division computer science requirements not met. {element} not taken.")
    if not any(
        isinstance(course, dict) and course.get("Course", "").strip().upper() == "COM SCI 130" for course in taken_courses)\
        and not any(isinstance(course, dict) and course.get("Course", "").strip().upper() == "COM SCI 152B"
        for course in taken_courses
        ):
            raise ValueError(f"Upper division computer science requirements not met. You must take either COM SCI 130 or COM SCI 152B.")
    if any(
        isinstance(course, dict) and course.get("Course", "").strip().upper() == "COM SCI 130" for course in taken_courses)\
        and any(isinstance(course, dict) and course.get("Course", "").strip().upper() == "COM SCI 152B"
        for course in taken_courses
        ): #both taken, one as an elective, one as a requirement
            specified_elective_counter -= 1
    if any(
        isinstance(course, dict) and course.get("Course", "").strip().upper() == "COM SCI 130" for course in taken_courses)\
        ^ any(isinstance(course, dict) and course.get("Course", "").strip().upper() == "COM SCI 152B"
        for course in taken_courses
        ): #xor one taken, only as a requirement
            specified_elective_counter -= 1
    if not any(
        isinstance(course, dict) and course.get("Course", "").strip().upper() == "MATH 170A" for course in taken_courses)\
        and not any(isinstance(course, dict) and course.get("Course", "").strip().upper() == "170E"
        for course in taken_courses
        ): #probability requirement
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
        
    
async def executioner(eng_comp: bool = False):
    local_list = []

    already_taken = await upload_previous_courses()  
    local_list.extend(already_taken)
    future = await upload_future_courses()  
    local_list.extend(future)
    
    
    '''
    if duplicates:
        print(f"Found {len(duplicates)} duplicate(s) based on course_name:")
        for dup in duplicates:
            print(f"- Duplicate: {dup.get('course_name')} ({dup.get('catalog_year')})")
    '''

    print(f"Total courses: {len(local_list) + len(already_taken)}")
    
    lowest = find_lowest_quarter(local_list)
    if not lowest:
        return local_list, False  # no sorting if no valid quarters found
    start_year, start_quarter_idx = lowest
    quarter_sequence = generate_quarter_sequence(start_year, start_quarter_idx)    
    priority_map = {q: i for i, q in enumerate(quarter_sequence)}
    local_list.sort(key=lambda c: priority_map.get(c.get("catalog_year", ""), 9999))

    validity = await isValid(already_taken, local_list, eng_comp)

    return local_list, validity


async def main():
    local_list, validity = await executioner(False)
    if validity:
        print("The list satisfies CS requirements")
    else:
        print("The list is invalid")
    for item in local_list:
        print(item.get('Course'), item.get('Quarter'))

if __name__ == "__main__":
    asyncio.run(main())
