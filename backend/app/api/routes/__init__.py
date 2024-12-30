from .health import router as health_router
from .resume import router as resume_router
from .applications import router as applications_router

__all__ = ["health_router", "resume_router", "applications_router"]