import os
from fastapi import Header, HTTPException
from dotenv import load_dotenv
load_dotenv()

# Make sure you have a .env file with the ADMIN_KEY variable set
# Some endpoints will require this key for access
ADMIN_KEY = os.getenv("ADMIN_KEY")  

async def validate_admin_key(x_api_key: str = Header(...)):
    if x_api_key != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True