from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import spacy
from ...database import get_db
from .. import models, schemas
import docx2txt
import PyPDF2
import io
import os
from datetime import datetime

router = APIRouter(
    prefix="/resumes",
    tags=["resumes"]
)

nlp = spacy.load("en_core_web_lg")

@router.post("/", response_model=schemas.Resume)
async def create_resume(
    title: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    
    # Save file
    file_path = os.path.join("uploads", f"{datetime.now().timestamp()}_{file.filename}")
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

@router.get("/", response_model=List[schemas.Resume])
def get_resumes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    resumes = db.query(models.Resume).offset(skip).limit(limit).all()
    return resumes