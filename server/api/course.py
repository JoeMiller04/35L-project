from fastapi import APIRouter, HTTPException, Depends
from server.models.course import Course, CourseCreate, CourseResponse, CourseUpdate
from server.db.mongodb import course_collection
from bson import ObjectId
from bson.errors import InvalidId
from typing import List
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

