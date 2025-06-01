from fastapi import APIRouter, HTTPException, Depends
from server.models.course import Course, CourseCreate, CourseResponse, CourseUpdate
from server.db.mongodb import course_collection
from bson import ObjectId
from bson.errors import InvalidId
from typing import List, Optional
from server.api.security import validate_admin_key

router = APIRouter()


@router.post("/courses", response_model=CourseResponse, dependencies=[Depends(validate_admin_key)])
async def create_course(course_item: CourseCreate):
    """
    Create a new course
    TODO Check if the course already exists
    """
    course_dict = course_item.model_dump()
    result = await course_collection.insert_one(course_dict)
    created_course = await course_collection.find_one({"_id": result.inserted_id})
    
    if created_course is None:
        raise HTTPException(status_code=404, detail="Course creation failed")
    
    # Convert ObjectId to string
    if created_course and "_id" in created_course:
        created_course["_id"] = str(created_course["_id"])
    
    return created_course


@router.get("/courses/{course_id}", response_model=CourseResponse)
async def read_course(course_id: str):
    """
    Get a course by ID.
    Returns the course object if found.
    Otherwise, raises HTTPException 404 or 400.
    """
    try:
        oid = ObjectId(course_id)
        course = await course_collection.find_one({"_id": oid})
        if course is None:
            raise HTTPException(status_code=404, detail="Course not found")
            
        # Convert ObjectId to string
        if "_id" in course:
            course["_id"] = str(course["_id"])
        
        return course
    except InvalidId:  # Specific exception for invalid ObjectId format
        raise HTTPException(status_code=400, detail="Invalid ID format")
    except Exception as e:
        # For other exceptions, check if it's already an HTTPException
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
    

@router.put("/courses/{course_id}", response_model=CourseResponse, dependencies=[Depends(validate_admin_key)])
async def update_course(course_id: str, course_update: CourseUpdate):
    """
    Update a course
    """
    try:
        oid = ObjectId(course_id)
        
        # Filter out None values
        # We only want to update fields that are provided
        update_data = {k: v for k, v in course_update.model_dump().items() if v is not None}
        
        # If there's nothing to update
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid update data provided")
        
        # Update the course
        result = await course_collection.update_one(
            {"_id": oid},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Course not found")
        
        # Return the updated course
        updated_course = await course_collection.find_one({"_id": oid})
        if updated_course is None:
            raise HTTPException(status_code=500, detail="Database error: Course not found after update")
        updated_course["_id"] = str(updated_course["_id"])
        
        return updated_course
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")

@router.delete("/courses/{course_id}", status_code=204, dependencies=[Depends(validate_admin_key)])
async def delete_course(course_id: str):
    """
    Requires admin key in headers.
    Delete a course by ID.
    Returns 204 No Content on success.
    Otherwise, raises HTTPException 404 or 400.
    """
    try:
        oid = ObjectId(course_id)
        result = await course_collection.delete_one({"_id": oid})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Course not found")
        
        return None # 204 No Content, Successful deletion
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")


@router.get("/courses", response_model=List[CourseResponse])
async def query_courses(
    term: Optional[str] = None,
    subject: Optional[str] = None,
    catalog: Optional[str] = None,
    instructor: Optional[str] = None,
    title: Optional[str] = None,
    real: Optional[bool] = None,
    skip: int = 0,
    limit: int = 20,
):
    """
    Query courses with optional filters.
    
    Parameters:
    - term: Filter by term (e.g., "22F")
    - subject: Filter by subject (e.g., "COM SCI")
    - catalog: Filter by catalog number (e.g., "35L")
    - instructor: Filter by instructor name (partial match, case insensitive)
    - title: Filter by course title (partial match, case insensitive)
    - real: Filter by whether the course is real or test data
    - skip: Number of records to skip (for pagination)
    - limit: Maximum number of records to return

    skip and limit can be used if you want to read a subset of the courses.
    E.g. Pagesize of 20, skip 0 for the first page, skip 20 for the second page, etc.
    
    Returns a list of courses matching the criteria.
    """
    try:
        # Build query filter
        query = {}
        
        if term:
            query["term"] = term
        if subject:
            query["subject"] = subject
        if catalog:
            query["catalog"] = catalog
        if instructor:
            # Case-insensitive partial match for instructor
            query["instructor"] = {"$regex": instructor, "$options": "i"}
        if title:
            # Case-insensitive partial match for title
            query["title"] = {"$regex": title, "$options": "i"}
        if real is not None:  # Explicitly check if it's None since false is a valid value
            query["real"] = real
        
        # Count total matching documents for pagination info
        total_count = await course_collection.count_documents(query)
        
        # Execute the query with pagination
        cursor = course_collection.find(query).skip(skip).limit(limit)
        courses = await cursor.to_list(length=limit)
        
        # Convert ObjectIds to strings
        for course in courses:
            course["_id"] = str(course["_id"])
        
        return courses
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying courses: {str(e)}")


@router.get("/courses/catalogs/{subject}", response_model=List[str])
async def get_catalogs_by_subject(subject: str):
    """
    Get all unique catalog numbers for a specific subject.
    If subject is not found, returns an empty list.
    subject is case-insensitive.
    Parameters:
    - subject: Course subject (e.g., "COM SCI")
    
    Returns:
    - List of unique catalog numbers for the given subject, kind of sorted
    """
    try:
        subject = subject.upper()
        catalogs = await course_collection.distinct(
            "catalog", 
            {"subject": subject}
        )
        
        # I try to sort the catalog numbers in a relatively natural way
        def catalog_sort_key(catalog):
            """
            Custom sort key function that handles catalog numbers like:
            - Pure numbers: "180", "101"
            - Numbers with suffix: "35L", "97A"
            - Prefixed letters: "M51", "CS32"
            """
            numeric_part = ''
            prefix = ''
            suffix = ''
            
            if catalog and catalog[0].isalpha():
                i = 0
                while i < len(catalog) and catalog[i].isalpha():
                    prefix += catalog[i]
                    i += 1
                catalog = catalog[i:]
            
            # Extract the numeric part
            i = 0
            while i < len(catalog) and catalog[i].isdigit():
                numeric_part += catalog[i]
                i += 1
            
            # Remaining characters are the suffix
            suffix = catalog[i:] if i < len(catalog) else ''
            
            # Convert numeric part to int for proper numeric sorting
            # If no numeric part, use 0
            numeric_value = int(numeric_part) if numeric_part else 0
            
            # Return a tuple for sorting: (numeric_value, prefix, suffix)
            # This ensures sorting first by number, then by prefix, then by suffix
            return (numeric_value, prefix, suffix)
        
        # Sort using the custom key function
        catalogs.sort(key=catalog_sort_key)
        
        return catalogs
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error retrieving catalogs for subject {subject}: {str(e)}"
        )


@router.get("/subjects", response_model=List[str])
async def get_all_subjects():
    """
    Get all unique course subjects.
    
    Returns:
    - List of unique course subjects
    """
    try:
        subjects = await course_collection.distinct("subject")
        
        # Sort subjects alphabetically
        subjects.sort()
        
        return subjects
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error retrieving subjects: {str(e)}"
        )