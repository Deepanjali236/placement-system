from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.etl import transform

router = APIRouter(prefix="/upload", tags=["Excel Bulk Upload"])

@router.post("/excel")
async def upload_excel_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Block invalid MIME types
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Invalid file extension. Please upload an Excel document.")
        
    try:
        contents = await file.read()
        result = transform.process_excel_upload(contents, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing ETL pipeline: {str(e)}")