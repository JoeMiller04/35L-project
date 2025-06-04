from server.models.user import PyObjectId
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson import ObjectId


class Description(BaseModel):
    """
    Description model for MongoDB
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # MongoDB ObjectId
    subject: str  # Course subject, e.g., "COM SCI"
    catalog: str  # Course catalog number, e.g., "35L"
    title: str   # Course title, e.g., "Introduction to Computer Science"
    description: str  # Course description, e.g., "An introduction to the fundamentals of computer science."
    units: str # Course units, e.g., "4 units"
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )