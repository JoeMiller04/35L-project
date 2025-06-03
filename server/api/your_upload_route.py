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
    
    try:
        print("Starting upload")
        upload_dir = "server/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)   
        print("Completed upload")

        print("Calling script")
        script_path = os.path.abspath("server/data/Dars/dars-parser.py")
        result = subprocess.run(
            [sys.executable, script_path, file_path, user_id],
            capture_output=True,
            text=True
        )
        print("Completed script call")
        

        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Parser error: {result.stderr}")

        # 3. Return the output (JSON) from dars-parser.py
        # Is this for debugging or production?
        return "Test"
        return {"filename": file.filename, "dars_output": json.loads(result.stdout)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))