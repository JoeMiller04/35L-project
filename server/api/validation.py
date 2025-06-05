from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from server.services.new_planner_check import executioner

router = APIRouter()

class PlanValidationResponse(BaseModel):
    valid: bool
    message: str

    # It's helpful for debugging

@router.post("/validate-plan/{user_id}", response_model=PlanValidationResponse)
async def validate_plan(
    user_id: str = Path(..., description="The user ID"),
    eng_comp: bool = False
):
    """
    Validate a user's course plan
    Returns validation status and sorted course list
    """
    try:
        result = await executioner(user_id, eng_comp)
        
        return {
            "validity": result["validity"],
            "message": "Your course plan meets all CS degree requirements!" if result["validity"] 
                      else "Your course plan does not meet all requirements.",
        }
    except ValueError as e:
        # Handle expected validation errors from the planner check
        return {
            "valid": False,
            "message": str(e),

        }
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500, 
            detail=f"Error validating course plan: {str(e)}"
        )