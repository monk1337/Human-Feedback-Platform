from fastapi import APIRouter, Response, Request

from src.authentication.auth_model import OTPModel, UserModel
from src.authentication.auth_controller import store_otp, validate_otp, get_user_from_role, verify_user_logged_in, change_verify_status
from src.jwt.jwt import create_access_token, decode_access_token
from src.jwt.model import TokenPayload
router = APIRouter()

@router.post("/send-otp")
def send_otp(otp_data: OTPModel):
    otp = store_otp(otp_data.mobile)

    return otp

@router.post("/verify-otp")
def verify_otp_router(otp_data: OTPModel):
    validate_otp(otp_data)

    return {"message": "Success"}

@router.post("/verify-user")
def verify_user(user: UserModel):
    get_user_from_role(user)
    return {"message": "Success"}

@router.post("/auth/login")
def login(response: Response, user: UserModel):
    verify_user_logged_in(user)
    change_verify_status(user.mobile)

    payload = TokenPayload(mobile=user.mobile, role=user.role)
    jwt_token = create_access_token(payload)

    response.set_cookie(key="access_token", value=jwt_token, httponly=True, secure=True, samesite="none")
    return {"message": "User Logged in Successfully"}

@router.get("/auth/login")
def verify_login(request: Request):
    token = request.cookies.get("access_token")
    print(token)
    user = decode_access_token(token)

    return user

@router.get("/auth/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")

    return {"message": "Logged out successfully"}
