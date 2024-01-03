from fastapi import HTTPException
from passlib.context import CryptContext
from starlette.status import HTTP_409_CONFLICT

from src.authentication.auth_model import User
from src.db.db_config import db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def is_user_exist(mobile: str) -> bool :
    user = db.user.find_one({ "mobile": mobile })

    if(user):
        return True
    
    return False

def create_user(user: User):

    if(is_user_exist(user.mobile)):
        raise HTTPException(HTTP_409_CONFLICT, {"message": "User already exists"})

    db.user.insert_one(
        {
            "mobile": user.mobile,
            "password": get_password_hash(user.password)
        }
    )
