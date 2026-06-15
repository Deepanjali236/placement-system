from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class InterviewBase(BaseModel):
    student_id: int
    company: str
    interview_date: datetime
    status: Optional[str] = "Scheduled"

class InterviewCreate(InterviewBase):
    pass

class InterviewResponse(InterviewBase):
    id: int

    class Config:
        from_attributes = True