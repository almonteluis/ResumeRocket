from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    resumes = relationship("Resume", back_populates="owner")
    applications = relationship("JobApplication", back_populates="user")

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    file_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="resumes")
    analyses = relationship("ResumeAnalysis", back_populates="resume")

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String)
    position = Column(String)
    job_description = Column(Text)
    status = Column(String)  # Applied, Interview, Offer, Rejected, etc.
    date_applied = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)
    match_score = Column(Float, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=True)

    user = relationship("User", back_populates="applications")
    resume = relationship("Resume")
    analysis = relationship("ResumeAnalysis", back_populates="application")

class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    application_id = Column(Integer, ForeignKey("job_applications.id"))
    match_score = Column(Float)
    missing_keywords = Column(Text)  # Stored as JSON string
    suggested_modifications = Column(Text)  # Stored as JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    resume = relationship("Resume", back_populates="analyses")
    application = relationship("JobApplication", back_populates="analysis")