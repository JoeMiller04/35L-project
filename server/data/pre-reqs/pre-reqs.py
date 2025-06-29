#!/usr/bin/env python3

from collections import namedtuple
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")


Prerequisite = namedtuple("Prerequisite", ["units", "elective_eligible", "requisites", "aliases"])
Reverse_aliases = namedtuple("Alternate_name", "Main_name")

def make_alias(alias_name):
    return alias_name

def reverse_aliases():
    aliases_key = {}
    aliases_key["EC ENGR M16"] = make_alias("COM SCI M51A")
    aliases_key["C&EE 110"] = make_alias("MATH 170A")
    aliases_key["EC ENGR 131A"] = make_alias("MATH 170A")
    aliases_key["STATS 100A"] = make_alias("MATH 170A")
    aliases_key["EC ENGR 132B"] = make_alias("COM SCI 118")
    aliases_key["EC ENGR M117"] = make_alias("COM SCI M138")
    aliases_key["EC ENGR M116L"] = make_alias("COM SCI M152A")

    aliases_list = []
    for alias, original_course in aliases_key.items():
        aliases_list.append({
            "alias_key": alias,
            "original_course": original_course
        })
    return aliases_list


def make_prereq(units, elective_eligible=False, requisites=None, aliases=None):
    if requisites is None:
        requisites = []
    if aliases is None:
        aliases = []
    return Prerequisite(units, elective_eligible, requisites, aliases)

def upload_classes():
    classes = {}

    # Use class_name as key; no class_name inside the object
    classes["COM SCI 1"] = make_prereq(1)
    classes["COM SCI 30"] = make_prereq(4)
    classes["COM SCI 31"] = make_prereq(4)
    classes["COM SCI 32"] = make_prereq(4, requisites=
        [
            [classes["COM SCI 31"]]
        ])
    classes["COM SCI 33"] = make_prereq(4, requisites=
        [
            [classes["COM SCI 31"], classes["COM SCI 32"]]
        ])
    classes["COM SCI 35L"] = make_prereq(4, requisites=
        [
            [classes["COM SCI 31"]]
        ])
    classes["COM SCI M51A"] = make_prereq(4, requisites=[
        [classes["COM SCI 31"]]], aliases=["EC ENGR M16"])

    # Math Lower Division
    classes["MATH 31A"] = make_prereq(4)
    classes["MATH 31B"] = make_prereq(4, requisites=
        [
            [classes["MATH 31A"]]
        ])
    classes["MATH 32A"] = make_prereq(4, requisites=
        [
            [classes["MATH 31A"]]
        ])
    classes["MATH 32B"] = make_prereq(4, requisites=
        [
            [classes["MATH 31B"], classes["MATH 32A"]]
        ])
    classes["MATH 33A"] = make_prereq(4, requisites=
        [
            [classes["MATH 31B"]], 
            [classes["MATH 32A"]]
        ])
    classes["MATH 33B"] = make_prereq(4, requisites=[[classes["MATH 31B"]]])
    classes["MATH 61"] = make_prereq(4)
    classes["MATH 170A"] = make_prereq(4, 
        aliases=["C&EE 110", "EC ENGR 131A", "STATS 100A"])
    classes["MATH 170E"] = make_prereq(4)

    # Physics Lower Division
    classes["PHYSICS 1A"] = make_prereq(5, requisites=
        [
            [classes["MATH 31A"], classes["MATH 31B"]]
        ])
    classes["PHYSICS 1B"] = make_prereq(5, requisites=
        [
            [classes["PHYSICS 1A"], classes["MATH 31B"], classes["MATH 32A"]]
        ])
    classes["PHYSICS 1C"] = make_prereq(5, requisites=
        [
            [classes["PHYSICS 1A"], classes["PHYSICS 1B"], classes["MATH 32A"], classes["MATH 32B"]]
        ])
    classes["PHYSICS 4AL"] = make_prereq(2)
    classes["PHYSICS 4BL"] = make_prereq(2)

    #Not required but other lower division classes
    classes["LIFESCI 30A"] = make_prereq(4)
    classes["LIFESCI 30B"] = make_prereq(4, requisites=
        [
            [classes["LIFESCI 30A"]]
        ])

    # CS Upper Division
    classes["COM SCI 111"] = make_prereq(5, requisites=
        [
            [classes["COM SCI 32"], classes["COM SCI 33"], classes["COM SCI 35L"]]
        ])
    classes["COM SCI 112"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 111"], classes["MATH 170A"]]
        ])
    classes["COM SCI 117"] = make_prereq(4, True)
    classes["COM SCI 118"] = make_prereq(4, requisites=[
        [classes["COM SCI 111"]]], aliases=["EC ENGR 132B"])
    classes["COM SCI M119"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 33"], classes["COM SCI 118"], classes["MATH 170E"]],
            [classes["COM SCI 33"], classes["COM SCI 118"], classes["MATH 170A"]]
        ])

    classes["COM SCI C121"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 32"], classes["MATH 170E"]],
            [classes["COM SCI 32"], classes["MATH 170A"]]
        ])
    classes["COM SCI C122"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 32"], classes["MATH 170E"]],
            [classes["COM SCI 32"], classes["MATH 170A"]]
        ])
    classes["COM SCI C124"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 32"], classes["MATH 33A"], classes["MATH 170E"]],
            [classes["COM SCI 32"], classes["MATH 33A"], classes["MATH 170A"]]
        ])
    classes["COM SCI 131"] = make_prereq(4, False, requisites=
        [
            [classes["COM SCI 33"], classes["COM SCI 35L"]]
        ])
    classes["COM SCI 130"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 111"], classes["COM SCI 131"]]
        ])
    classes["COM SCI 132"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 131"]]
        ])
    classes["COM SCI M151B"] = make_prereq(4, requisites=
        [
            [classes["COM SCI M51A"], classes["COM SCI 33"]]
        ])
    classes["COM SCI 133"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 131"], classes["COM SCI M151B"]]
        ])
    classes["COM SCI 134"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 118"]]
        ])
    classes["COM SCI 136"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 118"]]
        ])
    classes["COM SCI C137A"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 131"]]
        ])
    classes["COM SCI C137B"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI C137A"]]
        ])
    classes["COM SCI M138"] = make_prereq(4, True, requisites=[
        [classes["COM SCI 33"]]], aliases=["EC ENGR M117"])
    classes["COM SCI 143"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 32"]]
        ])
    classes["COM SCI 144"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 32"]]
        ])
    classes["COM SCI 145"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 32"]]
        ])
    classes["COM SCI M146"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 32"], classes["MATH 33A"], classes["MATH 170E"]],
            [classes["COM SCI 32"], classes["MATH 33A"], classes["MATH 170A"]]
        ])
    classes["COM SCI M148"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 31"], classes["MATH 170E"]],
            [classes["COM SCI 31"], classes["MATH 170A"]]
        ])
    classes["COM SCI M152A"] = make_prereq(2, requisites=[
        [classes["COM SCI M51A"]]], aliases=["EC ENGR M116L"])
    classes["COM SCI 152B"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI M151B"]]
        ])
    classes["COM SCI 180"] = make_prereq(4, requisites=
        [
            [classes["COM SCI 32"], classes["MATH 61"]]
        ])
    classes["COM SCI 161"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 180"]]
        ])
    classes["COM SCI 162"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 145"]],
            [classes["COM SCI M146"]]
        ])
    classes["COM SCI 163"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI C124"]],
            [classes["COM SCI 145"]],
            [classes["COM SCI M146"]],
            [classes["COM SCI M148"]],
            [classes["COM SCI 161"]],
            [classes["COM SCI 162"]]
        ])
    classes["COM SCI 168"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 32"], classes["MATH 33A"], classes["MATH 170E"]],
            [classes["COM SCI 32"], classes["MATH 33A"], classes["MATH 170A"]]
        ])
    classes["COM SCI 170A"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 180"], classes["MATH 33B"]]
        ])
    classes["COM SCI M171L"] = make_prereq(4, True)
    classes["COM SCI 172"] = make_prereq(4, requisites=
        [
            [classes["COM SCI 32"]]
        ])
    classes["COM SCI 174A"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 32"]]
        ])
    classes["COM SCI 174B"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 174A"]]
        ])
    classes["COM SCI C174C"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 174A"]]
        ])
    classes["COM SCI 181"] = make_prereq(4, requisites=
        [
            [classes["COM SCI 180"]]
        ])
    classes["COM SCI M182"] = make_prereq(4, True, requisites=
        [
            [classes["LIFESCI 30A"], classes["LIFESCI 30B"], classes["MATH 31A"], classes["MATH 31B"]],
        ])
    classes["COM SCI 183"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI 180"]]
        ])
    classes["COM SCI M184"] = make_prereq(2, True, requisites=
        [
            [classes["COM SCI 31"], classes["MATH 31B"]]
        ])
    classes["COM SCI CM186"] = make_prereq(5, True, requisites=
        [
            [classes["LIFESCI 30A"], classes["LIFESCI 30B"], classes["MATH 32A"], classes["MATH 33A"], classes["MATH 33B"]],
        ])
    classes["COM SCI CM187"] = make_prereq(4, True, requisites=
        [
            [classes["COM SCI M182"]], 
            [classes["COM SCI CM186"]]
        ])
    classes["COM SCI 188"] = make_prereq(4)

    return classes


def serialize_prereq(prereq, reverse_map):
    """
    Serialize a Prerequisite namedtuple to a dict for MongoDB.
    Converts requisites (list of list of Prerequisite) into lists of course names using reverse_map.
    """
    return {
        "units": prereq.units,
        "elective_eligible": prereq.elective_eligible,
        "requisites": [
            [reverse_map[id(c)] for c in group]
            for group in prereq.requisites
        ],
        "aliases": prereq.aliases,
    }

def export_to_mongodb(classes):
    if not MONGO_URI or not DATABASE_NAME:
        print("MONGO_URI or DATABASE_NAME is not set in the environment variables.")
        return

    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db["pre-reqs"]
    aliases_collection = db["Aliases"]

    reverse_map = {id(v): k for k, v in classes.items()}

    serialized_docs = []
    for course_name, prereq in classes.items():
        serialized = serialize_prereq(prereq, reverse_map)
        serialized["course_name"] = course_name
        serialized_docs.append(serialized)
        
    collection.delete_many({})

    result = collection.insert_many(serialized_docs)


    aliases = reverse_aliases()

    aliases_collection.delete_many({})
    new_result = aliases_collection.insert_many(aliases)

    print(f"Inserted {len(result.inserted_ids)+len(new_result.inserted_ids)} documents.")
    
    client.close()
    
    '''
    Tester for printing
    classes = upload_classes()
    
    # Create reverse lookup by object id
    reverse_map = {id(v): k for k, v in classes.items()}
    
    for name, course in classes.items():
        if not course.requisites:
            prereq_names = []
        else:
            # Look up by id to get the string course names
            prereq_names = [
                [reverse_map[id(c)] for c in group]
                for group in course.requisites
            ]
        print(f"{name}: Prereq groups: {prereq_names}")
    '''

if __name__ == "__main__":
    classes = upload_classes()
    export_to_mongodb(classes)
