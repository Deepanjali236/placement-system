from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.models.interview import Interview
from app.schemas.interview import InterviewCreate, InterviewResponse

router = APIRouter(prefix="/interviews", tags=["Interview Scheduler"])

@router.post("/", response_model=InterviewResponse)
def schedule_interview(interview: InterviewCreate, db: Session = Depends(get_db)):
    db_interview = Interview(
        student_id=interview.student_id,
        company=interview.company,
        interview_date=interview.interview_date,
        status=interview.status
    )
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    return db_interview

@router.get("/", response_model=List[InterviewResponse])
def get_all_interviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Interview).offset(skip).limit(limit).all()