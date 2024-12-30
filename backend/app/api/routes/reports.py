from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from ...database import get_db
from ...services.report_generator import ResumeReportGenerator
from .. import models

router = APIRouter(
    prefix="/reports",
    tags=["reports"]
)

report_generator = ResumeReportGenerator()

@router.get("/{analysis_id}")
async def generate_report(
    analysis_id: int,
    report_type: Optional[str] = "detailed",
    db: Session = Depends(get_db)
):
    """Generate a report for a specific analysis."""
    analysis = db.query(models.ResumeAnalysis).filter(
        models.ResumeAnalysis.id == analysis_id
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    try:
        analysis_data = json.loads(analysis.analysis_data)
        report = report_generator.generate_report(analysis_data, report_type)
        return report
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating report: {str(e)}"
        )