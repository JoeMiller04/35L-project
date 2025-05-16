from pydantic import BaseModel, Field, GetJsonSchemaHandler, GetCoreSchemaHandler, ConfigDict
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from bson import ObjectId
from typing import Optional, Any, Annotated, List


class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.str_schema(pattern="^[0-9a-f]{24}$")
    
    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


class User(BaseModel):
    """
    User model for MongoDB
    """
    id: Optional[PyObjectId] = Field(alias="_id")
    username: str
    password_hash: str
    saved_courses: List[str] = []  # List of course names saved by the user

    # Updated configuration syntax for Pydantic v2
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )


class UserCreate(BaseModel):
    username: str
    password: str
    saved_courses: List[str] = []  # Optional during creation


class UserResponse(BaseModel):
    """
    User model for API response. Does not include password.
    """
    id: Optional[PyObjectId] = Field(alias="_id")
    username: str
    saved_courses: List[str] = [] 
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )


class UserCourseUpdate(BaseModel):
    """
    Model for adding or removing courses from a user's list
    """
    course_name: str # For now, we're just doing coursenames, not the actual course IDs
    action: str  # "add" or "remove"

