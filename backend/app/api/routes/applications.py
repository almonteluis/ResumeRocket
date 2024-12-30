from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import json
import spacy
from ...database import get_db
from .. import models, schemas
import docx2txt
import PyPDF2
import io
import os
from datetime import datetime

router = APIRouter()
nlp = spacy.load("en_core_web_lg")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/resumes/", response_model=schemas.Resume)
async def create_resume(
    title: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Save file
    file_path = os.path.join(UPLOAD_DIR, f"{datetime.now().timestamp()}_{file.filename}")
    content = await file.read()
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Extract text content
    if file.filename.endswith('.docx'):
        text_content = docx2txt.process(io.BytesIO(content))
    elif file.filename.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        text_content = ""
        for page in pdf_reader.pages:
            text_content += page.extract_text()
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")
    
    # Create resume record
    db_resume = models.Resume(
        title=title,
        content=text_content,
        file_path=file_path,
        user_id=1  # TODO: Get from authenticated user
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

@router.post("/resumes/analyze/", response_model=schemas.ResumeAnalysis)
async def analyze_resume(
    resume_id: int,
    application_id: int,
    db: Session = Depends(get_db)
):
    resume = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    application = db.query(models.JobApplication).filter(
        models.JobApplication.id == application_id
    ).first()
    
    if not resume or not application:
        raise HTTPException(status_code=404, detail="Resume or application not found")
    
    # Analyze match
    resume_doc = nlp(resume.content)
    job_doc = nlp(application.job_description)
    
    # Extract key terms
    job_keywords = set()
    for token in job_doc:
        if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop:
            job_keywords.add(token.text.lower())
    
    resume_keywords = set()
    for token in resume_doc:
        if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop:
            resume_keywords.add(token.text.lower())
    
    # Calculate match score
    matching_keywords = job_keywords.intersection(resume_keywords)
    missing_keywords = list(job_keywords - resume_keywords)
    
    score = len(matching_keywords) / len(job_keywords) if job_keywords else 0
    
    # Generate suggestions
    suggestions = [
        f"Consider adding experience with {keyword}" for keyword in missing_keywords[:5]
    ]
    
    # Create analysis record
    analysis = models.ResumeAnalysis(
        resume_id=resume_id,
        application_id=application_id,
        match_score=score * 100,
        missing_keywords=json.dumps(missing_keywords),
        suggested_modifications=json.dumps(suggestions)
    )
    
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    
    return analysis

@router.get("/resumes/", response_model=List[schemas.Resume])
def get_resumes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    resumes = db.query(models.Resume).offset(skip).limit(limit).all()
    return resumes