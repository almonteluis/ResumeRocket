from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class ResumeBase(BaseModel):
    title: str

class ResumeCreate(ResumeBase):
    content: Optional[str] = None

class Resume(ResumeBase):
    id: int
    file_path: str
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        from_attributes = True

class JobApplicationBase(BaseModel):
    company: str
    position: str
    job_description: str
    status: str = "Applied"
    notes: Optional[str] = None

class JobApplicationCreate(JobApplicationBase):
    resume_id: Optional[int] = None

class JobApplication(JobApplicationBase):
    id: int
    date_applied: datetime
    match_score: Optional[float] = None
    user_id: int
    resume_id: Optional[int] = None

    class Config:
        from_attributes = True

class ResumeAnalysisBase(BaseModel):
    match_score: float
    missing_keywords: List[str]
    suggested_modifications: List[str]

class ResumeAnalysisCreate(ResumeAnalysisBase):
    resume_id: int
    application_id: int

class ResumeAnalysis(ResumeAnalysisBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None