# ResumeRocket 🚀

ResumeRocket is an intelligent resume management and job application tracking system that helps you optimize your job search process. It analyzes your resume against job descriptions, provides tailored recommendations, and keeps track of your job applications all in one place.

## Features ✨

- **Resume Analysis**: AI-powered resume scanning that matches your skills with job requirements
- **Intelligent Recommendations**: Get suggestions to improve your resume for specific job applications
- **Application Tracking**: Keep track of all your job applications, their statuses, and important dates
- **Multiple Resume Versions**: Manage different versions of your resume for different types of positions
- **Modern UI**: Clean, responsive interface built with Next.js and shadcn/ui
- **Secure Backend**: FastAPI-powered backend with SQL database

## Tech Stack 🛠️

### Backend

- FastAPI (Python 3.8+)
- SQLAlchemy (Database ORM)
- spaCy (Natural Language Processing)
- PyPDF2 & docx2txt (Document Processing)
- SQLite (Database)

### Frontend

- Next.js 14
- TypeScript
- Tailwind CSS
- shadcn/ui
- React Query

## Getting Started 🚀

### Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn
- Git

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/resumerocket.git
cd resumerocket
```

2. Set up the backend:

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_lg

# Create .env file (use the template from .env.example)
cp .env.example .env

# Start the backend server
uvicorn app.main:app --reload
```

3. Set up the frontend:

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

4. Open your browser and navigate to:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Project Structure 📁

```
resumerocket/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   ├── models.py
│   │   │   └── schemas.py
│   │   ├── main.py
│   │   └── database.py
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── app/
│   │   └── styles/
│   ├── package.json
│   └── README.md
│
└── README.md
```

## API Documentation 📚

Detailed API documentation is available at `http://localhost:8000/docs` when running the backend server. The API includes endpoints for:

- Resume Management
- Job Application Tracking
- Resume Analysis
- Application Status Updates

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Roadmap 🗺️

- [ ] User authentication and authorization
- [ ] Enhanced resume analysis with industry-specific recommendations
- [ ] Email notifications for application status changes
- [ ] Interview scheduling and tracking
- [ ] Resume version control and comparison
- [ ] Integration with job boards
- [ ] Mobile app development

## License 📝

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/)
- [shadcn/ui](https://ui.shadcn.com/)
- [spaCy](https://spacy.io/)

## Support 💬

If you have any questions or need help with setup, please open an issue in the GitHub repository.

---

Built with ❤️ by Jorge Luis Almonte
