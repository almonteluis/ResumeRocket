from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection
        result = db.execute(text("SELECT 1")).fetchone()
        if result[0] == 1:
            return {
                "status": "healthy",
                "database": "connected",
                "details": {
                    "database_type": "postgresql",
                    "connection": "successful"
                }
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }