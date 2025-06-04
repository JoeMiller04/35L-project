from fastapi import APIRouter, HTTPException
from bson import ObjectId
from server.db.mongodb import descriptions_collection
from server.models.description import Description

router = APIRouter()

@router.get("/description/{subject}/{catalog}", response_model=Description)
async def get_description(subject: str, catalog: str):
    """
    Get a description and units for a specific course.
    Subject and catalog are case-insensitive (will be converted to uppercase).
    
    Parameters:
    - subject: Course subject (e.g., "COM SCI", "com sci", or "Com Sci")
    - catalog: Course catalog number (e.g., "35L", "35l")
    
    Returns:
    - Description object with subject, catalog, title, description, and units
    
    Raises:
    - 404 Not Found if no description doesn't exist for the specified course
    """
    try:
        # Convert subject and catalog to uppercase for case-insensitive matching
        subject_upper = subject.upper()
        catalog_upper = catalog.upper()
        
        # Perform exact match query with uppercase values
        description = await descriptions_collection.find_one({
            "subject": subject_upper,
            "catalog": catalog_upper
        })
        
        # If no description is found, raise a 404 error
        if description is None:
            raise HTTPException(
                status_code=404, 
                detail=f"No description found for {subject} {catalog}"
            )
        
        # Convert ObjectId to string for JSON serialization
        if "_id" in description:
            description["_id"] = str(description["_id"])
            
        return description
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500, 
            detail=f"Error retrieving description: {str(e)}"
        )



