import secrets
import os

def generate_env_file():
    """Generate a secure .env file with random secret key."""
    
    env_content = f'''# Database Configuration
DATABASE_URL=sqlite:///./resume_tracker.db

# Security Configuration
SECRET_KEY={secrets.token_urlsafe(32)}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
'''
    
    # Write to .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("Generated .env file with secure random SECRET_KEY")

if __name__ == "__main__":
    generate_env_file()