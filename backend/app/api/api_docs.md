# Resume Tracker API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
*Note: Authentication is planned but not yet implemented. Currently, all endpoints use user_id=1*

## Endpoints

### Resumes

#### POST /resumes/
Upload a new resume.

**Request**
- Form Data:
  - `title`: string (required)
  - `file`: file (PDF or DOCX) (required)

**Response**
```json
{
  "id": 1,
  "title": "Software Engineer Resume",
  "file_path": "uploads/1640995200_resume.pdf",
  "created_at": "2024-12-29T10:00:00",
  "updated_at": "2024-12-29T10:00:00",
  "user_id": 1
}
```

#### POST /resumes/analyze/
Analyze a resume against a job application.

**Request**
- Query Parameters:
  - `resume_id`: integer (required)
  - `application_id`: integer (required)

**Response**
```json
{
  "id": 1,
  "match_score": 85.5,
  "missing_keywords": ["docker", "kubernetes", "aws"],
  "suggested_modifications": [
    "Consider adding experience with docker",
    "Consider adding experience with kubernetes",
    "Consider adding experience with aws"
  ],
  "created_at": "2024-12-29T10:00:00"
}
```

#### GET /resumes/
Get all resumes for the current user.

**Request**
- Query Parameters:
  - `skip`: integer (optional, default: 0)
  - `#### GET /resumes/ (continued)
- Query Parameters:
  - `limit`: integer (optional, default: 100)

**Response**
```json
[
  {
    "id": 1,
    "title": "Software Engineer Resume",
    "file_path": "uploads/1640995200_resume.pdf",
    "created_at": "2024-12-29T10:00:00",
    "updated_at": "2024-12-29T10:00:00",
    "user_id": 1
  }
]
```

### Job Applications

#### POST /applications/
Create a new job application.

**Request**
```json
{
  "company": "Tech Corp",
  "position": "Senior Software Engineer",
  "job_description": "Looking for an experienced developer...",
  "status": "Applied",
  "notes": "Applied through company website",
  "resume_id": 1
}
```

**Response**
```json
{
  "id": 1,
  "company": "Tech Corp",
  "position": "Senior Software Engineer",
  "job_description": "Looking for an experienced developer...",
  "status": "Applied",
  "date_applied": "2024-12-29T10:00:00",
  "notes": "Applied through company website",
  "match_score": null,
  "user_id": 1,
  "resume_id": 1
}
```

#### GET /applications/
Get all job applications for the current user.

**Request**
- Query Parameters:
  - `skip`: integer (optional, default: 0)
  - `limit`: integer (optional, default: 100)

**Response**
```json
[
  {
    "id": 1,
    "company": "Tech Corp",
    "position": "Senior Software Engineer",
    "job_description": "Looking for an experienced developer...",
    "status": "Applied",
    "date_applied": "2024-12-29T10:00:00",
    "notes": "Applied through company website",
    "match_score": 85.5,
    "user_id": 1,
    "resume_id": 1
  }
]
```

#### GET /applications/{application_id}
Get a specific job application.

**Request**
- Path Parameters:
  - `application_id`: integer (required)

**Response**
```json
{
  "id": 1,
  "company": "Tech Corp",
  "position": "Senior Software Engineer",
  "job_description": "Looking for an experienced developer...",
  "status": "Applied",
  "date_applied": "2024-12-29T10:00:00",
  "notes": "Applied through company website",
  "match_score": 85.5,
  "user_id": 1,
  "resume_id": 1
}
```

#### PUT /applications/{application_id}
Update a job application.

**Request**
- Path Parameters:
  - `application_id`: integer (required)
- Body:
```json
{
  "company": "Tech Corp",
  "position": "Senior Software Engineer",
  "job_description": "Updated job description...",
  "status": "Interview",
  "notes": "Phone interview scheduled"
}
```

**Response**
```json
{
  "id": 1,
  "company": "Tech Corp",
  "position": "Senior Software Engineer",
  "job_description": "Updated job description...",
  "status": "Interview",
  "date_applied": "2024-12-29T10:00:00",
  "notes": "Phone interview scheduled",
  "match_score": 85.5,
  "user_id": 1,
  "resume_id": 1
}
```

#### DELETE /applications/{application_id}
Delete a job application.

**Request**
- Path Parameters:
  - `application_id`: integer (required)

**Response**
```json
{
  "message": "Application deleted successfully"
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Data Models

### Resume
```typescript
{
  id: number;
  title: string;
  file_path: string;
  created_at: string; // ISO 8601 datetime
  updated_at: string; // ISO 8601 datetime
  user_id: number;
}
```

### Job Application
```typescript
{
  id: number;
  company: string;
  position: string;
  job_description: string;
  status: string; // "Applied" | "Interview" | "Offer" | "Rejected"
  date_applied: string; // ISO 8601 datetime
  notes?: string;
  match_score?: number;
  user_id: number;
  resume_id?: number;
}
```

### Resume Analysis
```typescript
{
  id: number;
  match_score: number;
  missing_keywords: string[];
  suggested_modifications: string[];
  created_at: string; // ISO 8601 datetime
}
```