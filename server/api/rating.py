from fastapi import APIRouter, HTTPException
from bson import ObjectId
from server.db.mongodb import ratings_collection
from server.models.rating import Rating

router = APIRouter()

@router.get("/ratings/{subject}/{catalog}", response_model=Rating)
async def get_rating(subject: str, catalog: str):
    """
    Get a rating for a specific course.
    Subject and catalog are case-insensitive (will be converted to uppercase).
    
    Parameters:
    - subject: Course subject (e.g., "COM SCI", "com sci", or "Com Sci")
    - catalog: Course catalog number (e.g., "35L", "35l")
    
    Returns:
    - Rating object with subject, catalog, and rating value
    
    Raises:
    - 404 Not Found if no rating exists for the specified course
    """
    try:
        # Convert subject and catalog to uppercase for case-insensitive matching
        subject_upper = subject.upper()
        catalog_upper = catalog.upper()
        
        # Perform exact match query with uppercase values
        rating = await ratings_collection.find_one({
            "subject": subject_upper,
            "catalog": catalog_upper
        })
        
        # If no rating is found, raise a 404 error
        if rating is None:
            raise HTTPException(
                status_code=404, 
                detail=f"No rating found for {subject} {catalog}"
            )
        
        # Convert ObjectId to string for JSON serialization
        if "_id" in rating:
            rating["_id"] = str(rating["_id"])
            
        return rating
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500, 
            detail=f"Error retrieving rating: {str(e)}"
        )


