# ResumeRocket Backend 🚀

FastAPI-powered backend for resume analysis and job application tracking.

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- spaCy (NLP)
- PyPDF2 & docx2txt
- Python 3.8+

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install NLP model
python -m spacy download en_core_web_lg

# Set up environment variables
cp .env.example .env
# Edit .env with your configurations

# Start server
uvicorn app.main:app --reload
```

## Project Structure
```
backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── analysis.py
│   │   │   ├── applications.py
│   │   │   └── resume.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── services/
│   │   ├── enhanced_analyzer.py
│   │   └── status_tracker.py
│   ├── main.py
│   ├── database.py
│   └── config.py
├── tests/
├── requirements.txt
└── .env
```

## API Endpoints

### Resume Management
- `POST /api/v1/resumes/`: Upload resume
- `GET /api/v1/resumes/`: List resumes
- `POST /api/v1/resumes/analyze/`: Analyze resume

### Job Applications
- `POST /api/v1/applications/`: Create application
- `GET /api/v1/applications/`: List applications
- `PUT /api/v1/applications/{id}`: Update application

### Analysis
- `POST /api/v1/analysis/`: Analyze resume against job description
- `GET /api/v1/analysis/{id}/report`: Generate analysis report

## Development

```bash
# Run tests
pytest

# Generate API documentation
python scripts/generate_openapi.py

# Database migrations
alembic revision --autogenerate
alembic upgrade head
```

## Environment Variables

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT secret key
- `API_V1_STR`: API version prefix
- `UPLOAD_DIR`: Directory for uploaded files
- `MAX_FILE_SIZE`: Maximum file size in bytes