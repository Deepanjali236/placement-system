from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.schemas.student import StudentCreate, StudentResponse
from app.services import student_service

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/", response_model=List[StudentResponse])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return student_service.get_students(db, skip=skip, limit=limit)

@router.post("/", response_model=StudentResponse)
def create_new_student(student: StudentCreate, db: Session = Depends(get_db)):
    return student_service.create_student(db=db, student=student)