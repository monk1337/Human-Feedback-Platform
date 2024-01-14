from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.utils.file_folder_handler import Folder_handler

load_dotenv()

@asynccontextmanager
async def lifespan(_: FastAPI):
    Folder_handler.create_folder()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://192.168.1.7:5173", "https://voicecord.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


router = APIRouter(prefix="/api")

@app.get("/")
def server_status():
    return {"Status": "Active"}

from src.authentication.auth_router import router as auth_router
router.include_router(auth_router)

from src.project.project_router import router as project_router
router.include_router(project_router)

app.include_router(router)
