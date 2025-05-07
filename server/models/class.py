from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from typing import Optional, List, Dict, Tuple
from server.models.user import PyObjectId  # Reuse ObjectId validator


# Define a type for the time schedule
TimeSchedule = Dict[str, Tuple[int, int]]


class Class(BaseModel):
    """
    Class model for MongoDB
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    real: bool = True  # Flag to differentiate real classes from test classes
    term: str  # e.g. "22F"
    subject: str  # e.g. "COM SCI"
    catalog: str  # e.g. "35L"
    title: str  # e.g. "Software Construction"
    instructor: str  # e.g. "Paul Eggert"
    times: Optional[TimeSchedule] = None  # Map of day to (start_time, end_time) in 24hr format
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )


class ClassCreate(BaseModel):
    """
    Model for creating a new class
    """
    real: bool = False  # Default to false, override for real classes
    term: str
    subject: str
    catalog: str
    title: str
    instructor: str
    times: Optional[TimeSchedule] = None  


class ClassResponse(BaseModel):
    """
    Class model for API response
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    term: str
    subject: str
    catalog: str
    title: str
    instructor: str
    real: bool
    times: Optional[TimeSchedule] = None  
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )


class ClassUpdate(BaseModel):
    """
    Model for updating an existing class
    """
    real: Optional[bool] = None
    term: Optional[str] = None
    subject: Optional[str] = None
    catalog: Optional[str] = None
    title: Optional[str] = None
    instructor: Optional[str] = None
    times: Optional[TimeSchedule] = None 

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )