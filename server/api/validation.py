from fastapi import APIRouter
from server.services.planner_check import isValid

router = APIRouter()

# This does not work right now
# Do not call, will crash server
@router.post("/validate-plan")
def validate_plan(plan: list):
    return isValid(plan)