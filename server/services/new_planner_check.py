#!/usr/bin/env python3

import sys
import os
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from server.db.mongodb import pre_reqs as reqs
from server.db.mongodb import previous_courses as pc
from server.db.mongodb import future_courses as fc
from server.db.mongodb import sample as sp
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
    
    quarters = ["w", "s", "f"]
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

async def isValid(sorted_list, eng_comp):
    taken_courses = []
    GE_counter = 0
    SCI_TECH_counter = 0
    TECH_BREADTH_counter = 0
    eng_comp_bool = eng_comp
    total_units = 0
    ethics_requirement = False
    for course in sorted_list:
        course_name = course.get('Course', '').strip()
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
        else:
            result = await reqs.find_one({"course_name": course_name})
            print (result)
            if not result:
                raise ValueError(f"Invalid course entry: {course_name}")

            # Add units
            units = result.get("units")
            if units is not None:
                total_units += units

            # Check pre-reqs
            requisite_courses = result.get("requisites", [])
            for group in requisite_courses:  # group is a list of course names
                if not any(pre_req in taken_courses for pre_req in group):
                    raise ValueError(f"Pre-requisite '{group}' for {course_name} not met")
            taken_courses.append(course_name)

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
        
    
async def executioner(eng_comp: bool):
    local_list = []

    previous = await upload_previous_courses()  
    local_list.extend(previous)
    future = await upload_future_courses()  
    local_list.extend(future)
    
    
    '''
    if duplicates:
        print(f"Found {len(duplicates)} duplicate(s) based on course_name:")
        for dup in duplicates:
            print(f"- Duplicate: {dup.get('course_name')} ({dup.get('catalog_year')})")
    '''

    print(f"Total deduplicated courses: {len(local_list)}")
    lowest = find_lowest_quarter(local_list)
    if not lowest:
        return local_list, False  # no sorting if no valid quarters found
    
    start_year, start_quarter_idx = lowest
    quarter_sequence = generate_quarter_sequence(start_year, start_quarter_idx)
    
    priority_map = {q: i for i, q in enumerate(quarter_sequence)}
    
    local_list.sort(key=lambda c: priority_map.get(c.get("catalog_year", ""), 9999))

    validity = await isValid(local_list, eng_comp)

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
