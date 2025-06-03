from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file to a directory (e.g., "uploads")
        upload_dir = "server/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"filename": file.filename, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))