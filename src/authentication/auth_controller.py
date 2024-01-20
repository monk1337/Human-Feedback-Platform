import math
import random
import time

from fastapi import HTTPException
from passlib.context import CryptContext
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

from src.authentication.auth_model import OTPModel, UserModel
from src.db.db_config import db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_otp_hash(plain_otp, hashed_otp):
    return pwd_context.verify(plain_otp, hashed_otp)

def get_otp_hash(otp):
    return pwd_context.hash(otp)

def is_resend_otp(user: dict) -> bool:
    curr_tiemstamp = math.ceil(time.time() * 1000)
    if(curr_tiemstamp < user["resend_timestamp"]):
        return False 
    return True

def generate_otp() -> int:
    return str(random.randint(1000,9999))

def store_otp(mobile: str) -> int:
    user = get_user(mobile)

    if(user != None and not is_resend_otp(user)):
        raise HTTPException(HTTP_400_BAD_REQUEST, {"message": "Please wait", "resend_timestamp": user["resend_timestamp"]})

    otp = generate_otp()
    resend_timestamp = math.ceil((time.time() + 60) * 1000) 
    data = {
        "otp": get_otp_hash(otp),
        "resend_timestamp": resend_timestamp,
        "verified": False
    }
    
    if(user == None):
        data["mobile"] = mobile
        db.users.insert_one(data)
    else:
        db.users.update_one(
            {
                "mobile": mobile
            },
            {
                "$set": data
            }
        )

    return {"otp": otp, "resend_timestamp": resend_timestamp}

def validate_otp(otp_data: OTPModel) -> dict:
    user = get_user(otp_data.mobile)

    if(user == None or not verify_otp_hash(otp_data.otp, user["otp"])):
        raise HTTPException(HTTP_400_BAD_REQUEST, {"message": "Invalid OTP"})
    
    db.users.update_one(
            {
                "mobile": otp_data.mobile
            },
            {
                "$set": {
                    "verified": True
                }
            }
        )
    
    return user

def get_user_from_role(user: UserModel):
    print(user)
    admin_filter_condition = {
        "admin_mobile": user.mobile
    }
    user_filter_condition = {}
    user_filter_condition[user.role] = {
        "$elemMatch": {
            "mobile": user.mobile
        }
    }

    filter_condition = {
        "$or": [admin_filter_condition, user_filter_condition]
    }

    project_count = db.projects.count_documents(filter_condition)

    if(project_count == 0):
        raise HTTPException(HTTP_404_NOT_FOUND, {"message": "No projects found"})

def verify_user_logged_in(user: UserModel) -> dict:
    curr_user = get_verified_user(user.mobile)

    if(curr_user == None):
        raise HTTPException(HTTP_401_UNAUTHORIZED, {"message": "User not Authenticated"})

    return curr_user

def change_verify_status(mobile: str): 
    db.users.update_one({"mobile": mobile}, {"$set": {"verified": False}});

def get_user(mobile: str) -> dict | None:
    return db.users.find_one({ "mobile": mobile })

def get_verified_user(mobile: str) -> dict | None:
    return db.users.find_one({ "mobile": mobile, "verified": True })

