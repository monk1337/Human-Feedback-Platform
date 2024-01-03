from fastapi import APIRouter

from src.authentication.auth_model import User
from src.authentication.auth_controller import create_user

router = APIRouter()

@router.post("/auth/signup", status_code=201)
def signup(user: User):
    create_user(user)

    return {"message": "User created successfully"}
