from pydantic import BaseModel
from typing import Optional

class StudentBase(BaseModel):
    roll_no: str
    name: str
    branch: str
    cgpa: float
    skills: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True