from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import subprocess
import sys
import json

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
      
        upload_dir = "server/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        

       
        script_path = os.path.abspath("server/data/Dars/dars-parser.py")
        result = subprocess.run(
            [sys.executable, script_path, file_path],
            capture_output=True,
            text=True
        )

        

        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Parser error: {result.stderr}")

        # 3. Return the output (JSON) from dars-parser.py
        return {"filename": file.filename, "dars_output": json.loads(result.stdout)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))