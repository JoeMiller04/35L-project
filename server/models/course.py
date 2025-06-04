from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from typing import Optional, List, Dict, Tuple
from server.models.user import PyObjectId  # Reuse ObjectId validator


# Define a type for the time schedule
TimeSchedule = Dict[str, Tuple[int, int]]


class Course(BaseModel):
    """
    Course model for MongoDB
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    real: bool = True  # Flag to differentiate real courses from test courses
    term: str  # e.g. "22F"
    subject: str  # e.g. "COM SCI"
    catalog: str  # e.g. "35L"
    title: str  # e.g. "Software Construction"
    instructor: str  # e.g. "Paul Eggert"
    times: Optional[TimeSchedule] = None  # Map of day to (start_time, end_time) in 24hr format

    section: Optional[str] = None  # This is not discussion section
    enrolled_total: Optional[int] = None  # Total number of students enrolled
    grades: Optional[Dict[str, int]] = None  # Grade distribution
    # Available grade keys: A+, A, A-, B+, B, B-, C+, C, C-, D+, D, D-, F
    # P, NP, other

    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )


class CourseCreate(BaseModel):
    """
    Model for creating a new course
    """
    real: bool = False  # Default to false, override for real courses
    term: str
    subject: str
    catalog: str
    title: str
    instructor: str
    times: Optional[TimeSchedule] = None  


class CourseResponse(BaseModel):
    """
    Course model for API response
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    term: str
    subject: str
    catalog: str
    title: str
    instructor: str
    real: bool
    times: Optional[TimeSchedule] = None

    grades: Optional[Dict[str, int]] = None  # Grade distribution  
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )


class CourseUpdate(BaseModel):
    """
    Model for updating an existing course
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