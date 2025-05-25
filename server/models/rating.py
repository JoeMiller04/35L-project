from server.models.user import PyObjectId
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson import ObjectId


class Rating(BaseModel):
    """
    Rating model for MongoDB
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # MongoDB ObjectId
    subject: str  # Course subject, e.g., "COM SCI"
    catalog: str  # Course catalog number, e.g., "35L"
    rating: float  # Rating value, e.g., 4.5

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )