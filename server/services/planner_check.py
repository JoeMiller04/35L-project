from server.utils.term import term_to_num #add later
from server.db.mongodb import valid_course_collection as db


def get_class_info(subject, catalog):
    return db.classes.find_one({"Subject": subject, "Catalog": catalog})

def prerequisites_satisfied(class_info, completed_classes):
    prerequisites = class_info.get("Requisites", [])
    return all(prereq in completed_classes for prereq in prerequisites)

def is_offered_in_term(class_info, term):
    offered_terms = class_info.get("OfferedTerms", [])
    return term in offered_terms

def isValid(plan: list) -> dict:
    completed_classes = set() # more like update schedule
    plan_sorted = sorted(plan, key=lambda p:term_to_num(p["term"]))

    for term_entry in plan_sorted:
        term = term_entry["term"]
        classes = term_entry["classes"]

        for class_name in classes:
            try:
                subject, catalog = class_name.split(" ", 1)
            except ValueError:
                return{"valid": False, "error": f"Invalid class format: {class_name}"}
            
            class_info = get_class_info(subject, catalog)
            if not class_info:
                return{"valid": False, "error": f"Class {class_name} not found"}
            
            if not is_offered_in_term(class_info, term):
                return{"valid": False, "error": f"{class_name} not offered in {term}"}
            
            if not prerequisites_satisfied(class_info, completed_classes):
                return{"valid": False, "error": f"Missing prerequisites for {class_name}"}
            

        completed_classes.update(classes)

    return{"valid": True}



