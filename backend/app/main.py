from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import analysis, resume, applications
from .api.websocket import handle_websocket
from .config import settings

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router)
app.include_router(resume.router)
app.include_router(applications.router)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await handle_websocket(websocket)