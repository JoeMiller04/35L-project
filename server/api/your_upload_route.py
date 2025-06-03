from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Path
import shutil
import os
import subprocess
import sys
import json

router = APIRouter()


@router.post("/users/{user_id}/upload")
async def upload_file(
    user_id: str = Path(..., description="The ID of the user"),
    file: UploadFile = File(...),
):
    
    
    filename = file.filename
    if filename is None:
        raise HTTPException(status_code=400, detail="Filename must be provided")
    file_extension = os.path.splitext(filename)[1].lower()
    if file_extension != ".html":
        raise HTTPException(status_code=400, detail="Only HTML files are allowed")
    upload_dir = "server/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)   
        
    try:
        script_path = os.path.abspath("server/data/Dars/dars-parser.py")
        result = subprocess.run(
            [sys.executable, script_path, file_path, user_id],
            capture_output=True,
            text=True
        )
        

        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Parser error: {result.stderr}")

        # 3. Return the output (JSON) from dars-parser.py
        # Is this for debugging or production?
        return "Test"

    except Exception as e:
        print(f"Error during file upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))