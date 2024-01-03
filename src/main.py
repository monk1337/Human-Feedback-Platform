from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api")

@app.get("/")
def server_status():
    return {"Status": "Active"}

from src.authentication.auth_router import router as auth_router
router.include_router(auth_router)

app.include_router(router)
