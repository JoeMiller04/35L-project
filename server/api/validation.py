from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel
from server.services.new_planner_check import executioner
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class PlanValidationResponse(BaseModel):
    valid: bool

@router.post("/validate-plan/{user_id}", response_model=PlanValidationResponse)
async def validate_plan(
    user_id: str = Path(..., description="The user ID")
):
    try:
        is_valid = await executioner(user_id)
        return PlanValidationResponse(valid=is_valid)

    except ValueError as e:
        return PlanValidationResponse(valid=False)

    except Exception as e:
        logger.error(f"Unexpected error in validate_plan: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during course plan validation."
        )