from fastapi import APIRouter, HTTPException
from bson import ObjectId
from server.db.mongodb import professor_ratings_collection
from server.models.professor_ratings import ProfessorRatings

router = APIRouter()

@router.get("/professor_ratings/{subject}/{catalog}", response_model=ProfessorRatings)
async def get_ratings(subject: str, catalog: str):
    """
    Get a professor ratings for a specific course.
    Subject and catalog are case-insensitive (will be converted to uppercase).
    
    Parameters:
    - subject: Course subject (e.g., "COM SCI", "com sci", or "Com Sci")
    - catalog: Course catalog number (e.g., "35L", "35l")
    
    Returns:
    - ProfessorRatings object with subject, catalog, and professors_and_ratings
    
    Raises:
    - 404 Not Found if no object exists for the specified course
    """
    try:
        # Convert subject and catalog to uppercase for case-insensitive matching
        subject_upper = subject.upper()
        catalog_upper = catalog.upper()
        
        # Perform exact match query with uppercase values
        professor_ratings = await professor_ratings_collection.find_one({
            "subject": subject_upper,
            "catalog": catalog_upper
        })
        
        # If no description is found, raise a 404 error
        if professor_ratings is None:
            raise HTTPException(
                status_code=404, 
                detail=f"No ratings found for {subject} {catalog}"
            )
        
        # Convert ObjectId to string for JSON serialization
        if "_id" in professor_ratings:
            professor_ratings["_id"] = str(professor_ratings["_id"])
            
        return professor_ratings
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500, 
            detail=f"Error retrieving description: {str(e)}"
        )


