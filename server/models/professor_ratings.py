from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from bson import ObjectId
from server.models.user import PyObjectId


class Professor(BaseModel):
    name: str
    rating: str


class ProfessorRatings(BaseModel):
    """
    Professor Ratings model for MongoDB
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # MongoDB ObjectId
    subject: str  # Course subject, e.g., "COM SCI"
    catalog: str  # Course catalog number, e.g., "35L"
    professors: List[Professor]  # List of professors and their ratings

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )