from pydantic import BaseModel
from typing import Optional, Literal

class OTPModel(BaseModel):
    mobile: str
    otp: Optional[str] = None

class UserModel(BaseModel):
    mobile: str
    role: Literal["recorder", "reviewer", "admin"]
