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
    professors_and_ratings: dict[str, float]  # Dictionary of professors and their ratings
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )