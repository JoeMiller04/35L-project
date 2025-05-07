from fastapi import APIRouter
from services.planner_check import isValid

router = APIRouter()

@router.post("/validate-plan")
def validate_plan(plan: list):
    return isValid(plan)