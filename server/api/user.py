from fastapi import APIRouter, Depends, HTTPException
from server.models.user import User, UserCreate, UserResponse, UserCourseUpdate, SavedCourse, CourseListUpdate
from server.db.mongodb import users_collection, course_collection
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from bson import ObjectId
from bson.errors import InvalidId
from server.api.security import validate_admin_key
from typing import Dict, List


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    """
    Creates a new user.
    Checks if the username already exists in the database.
    Returns 400 if it does.
    Otherwise, creates the user and returns the created user object.
    """
    existing = await users_collection.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = pwd_context.hash(user.password)

    user_data = {"username": user.username, "password_hash": hashed_password}

    new_user = await users_collection.insert_one(user_data)
    created_user = await users_collection.find_one({"_id": new_user.inserted_id})
    if created_user is None:
        raise HTTPException(status_code=404, detail="User creation failed")
    
    # Before returning, make sure the _id is converted to string
    if created_user and "_id" in created_user:
        created_user["_id"] = str(created_user["_id"])
    
    return created_user


@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: str):
    """
    Get a user by ID.
    Currently, users have no additional fields.
    Returns the user object if found.
    Otherwise, raises HTTPException 404 or 400.
    """
    try:
        oid = ObjectId(user_id)
        user = await users_collection.find_one({"_id": oid})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Convert ObjectId to string
        if "_id" in user:
            user["_id"] = str(user["_id"])
        
        return user
    except InvalidId:  # Specific exception for invalid ObjectId format
        raise HTTPException(status_code=400, detail="Invalid ID format")
    except Exception as e:
        # For other exceptions, check if it's already an HTTPException
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@router.post("/login", response_model=UserResponse)
async def login(username: str, password: str):
    """
    Simple login endpoint that verifies username/password
    and returns the user ID if successful.
    This is a temporary setup and let's improve it later.
    """
    # Find the user by username
    user = await users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username"
        )
    
    # Verify password
    if not pwd_context.verify(password, user["password_hash"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    
    if "_id" in user:
        user["_id"] = str(user["_id"])

    # Return user ID if authentication successful
    return user


@router.delete("/users/{user_id}", status_code=204, dependencies=[Depends(validate_admin_key)])
async def delete_user(user_id: str):
    """
    Requires admin key in headers.
    Delete a user by ID.
    Returns 204 No Content on success.
    Otherwise, raises HTTPException 404 or 400.
    """
    try:
        oid = ObjectId(user_id)
        result = await users_collection.delete_one({"_id": oid})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
            
        return None  # 204 No Content
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=400, detail=f"Invalid ID format: {str(e)}")


@router.post("/users/{user_id}/courses", response_model=UserResponse)
async def update_user_courses(user_id: str, update: UserCourseUpdate):
    """
    Add or remove a course from a user's saved courses list.
    Action field in the request body must be either "add" or "remove".
    Returns the updated user object.
    """
    try:
        oid = ObjectId(user_id)
        user = await users_collection.find_one({"_id": oid})
        
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Initialize saved_courses if it doesn't exist
        if "saved_courses" not in user:
            user["saved_courses"] = []
            
        # Create a saved course object
        saved_course = {"term": update.term, "course_name": update.course_name}
            
        # Process the update
        if update.action == "add":
            # Check if this term and course combination is already saved
            already_saved = False
            for course in user["saved_courses"]:
                if course.get("term") == update.term and course.get("course_name") == update.course_name:
                    already_saved = True
                    break
            
            # We don't return an error if the course is already saved
            if not already_saved:
                result = await users_collection.update_one(
                    {"_id": oid},
                    {"$push": {"saved_courses": saved_course}}
                )
                
        elif update.action == "remove":
            # Remove the specific term and course combination
            result = await users_collection.update_one(
                {"_id": oid},
                {"$pull": {"saved_courses": {
                    "term": update.term,
                    "course_name": update.course_name
                }}}
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid action. Use 'add' or 'remove'")
            
        # Get the updated user
        updated_user = await users_collection.find_one({"_id": oid})
        if updated_user and "_id" in updated_user:
            updated_user["_id"] = str(updated_user["_id"])
            
        return updated_user
        
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/users/{user_id}/courses", response_model=List[SavedCourse])
async def get_user_courses(user_id: str):
    """
    Get all courses saved by a user.
    Returns a list of SavedCourse objects containing term and course_name.
    """
    try:
        oid = ObjectId(user_id)
        user = await users_collection.find_one({"_id": oid})
        
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Check if user has saved courses
        if "saved_courses" not in user or not user["saved_courses"]:
            return []
        
        return user["saved_courses"]
        
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post("/users/{user_id}/course-list", response_model=UserResponse)
async def update_user_course_list(user_id: str, update: CourseListUpdate):
    """
    Add or remove a course ID from a user's course list.
    This is a simple bookmarking system that stores MongoDB course IDs.
    """
    try:
        oid = ObjectId(user_id)
        user = await users_collection.find_one({"_id": oid})
        
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Validate the course_id format
        try:
            course_oid = ObjectId(update.course_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid course ID format")
            
        # Check if the course exists
        course = await course_collection.find_one({"_id": course_oid})
        if course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        
        # Initialize course_list if it doesn't exist
        if "course_list" not in user:
            user["course_list"] = []
        
        # Convert all course IDs to strings for consistent comparison
        course_id_str = str(course_oid)
        user_course_list = [str(cid) for cid in user["course_list"]]
            
        if update.action == "add":
            # Add only if not already in the list
            if course_id_str not in user_course_list:
                result = await users_collection.update_one(
                    {"_id": oid},
                    {"$push": {"course_list": course_id_str}}
                )
                
                if result.modified_count == 0:
                    raise HTTPException(status_code=400, detail="Failed to add course to list")
                
        elif update.action == "remove":
            # Remove if present
            result = await users_collection.update_one(
                {"_id": oid},
                {"$pull": {"course_list": course_id_str}}
            )
            
        else:
            raise HTTPException(status_code=400, detail="Invalid action. Use 'add' or 'remove'")
            
        # Get the updated user
        updated_user = await users_collection.find_one({"_id": oid})
        if updated_user and "_id" in updated_user:
            updated_user["_id"] = str(updated_user["_id"])
            
        return updated_user
        
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/users/{user_id}/course-list", response_model=List[Dict])
async def get_user_course_list(user_id: str):
    """
    Get all courses in a user's course list.
    Returns the full course details for each course ID.
    """
    try:
        oid = ObjectId(user_id)
        user = await users_collection.find_one({"_id": oid})
        
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Check if user has a course list
        if "course_list" not in user or not user["course_list"]:
            return []
        
        # Get the full course details for each course ID
        result = []
        for course_id in user["course_list"]:
            try:
                course_oid = ObjectId(course_id)
                course = await course_collection.find_one({"_id": course_oid})
                
                if course:
                    # Convert ObjectId to string
                    course["_id"] = str(course["_id"])
                    result.append(course)
            except (InvalidId, Exception) as e:
                # Skip invalid entries but continue processing
                continue
                
        return result
        
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
