from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.db import Base
import datetime
from sqlalchemy.orm import relationship

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    company = Column(String, nullable=False)
    interview_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="Scheduled")  # Scheduled, Shortlisted, Placed, Rejected

    # Relationship to back-reference the Student table
    student = relationship("Student", back_populates="interviews")
    interviews = relationship("Interview", back_populates="student", cascade="all, delete-orphan")