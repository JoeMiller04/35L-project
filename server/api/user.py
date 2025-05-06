from fastapi import APIRouter, Depends, HTTPException
from server.models.user import User, UserCreate, UserResponse
from server.db.mongodb import users_collection
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from bson import ObjectId


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    """
    Create a new user.
    Checks if the username already exists in the database.
    """
    existing = await users_collection.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = pwd_context.hash(user.password)

    user_data = jsonable_encoder(user, exclude_none=True)
    user_data["password_hash"] = hashed_password
    new_user = await users_collection.insert_one(user_data)
    created_user = await users_collection.find_one({"_id": new_user.inserted_id})
    if created_user is None:
        raise HTTPException(status_code=404, detail="User creation failed")
    
    # Before returning, make sure the _id is converted to string
    if created_user and "_id" in created_user:
        created_user["_id"] = str(created_user["_id"])
    
    return created_user


@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: str):
    """
    Get a user by ID.
    """
    try:
        oid = ObjectId(user_id)
        user = await users_collection.find_one({"_id": oid})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    # Convert ObjectId to string
    if "_id" in user:
        user["_id"] = str(user["_id"])
    
    return user


@router.post("/login", response_model=UserResponse)
async def login(username: str, password: str):
    """
    Simple login endpoint that verifies username/password
    and returns the user ID if successful.
    This is a temporary setup and let's replace it later.
    """
    # Find the user by username
    user = await users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username"
        )
    
    # Verify password
    if not pwd_context.verify(password, user["password_hash"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    
    if "_id" in user:
        user["_id"] = str(user["_id"])

    # Return user ID if authentication successful
    return user

