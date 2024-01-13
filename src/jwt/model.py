from pydantic import BaseModel
from typing import Literal

class Token(BaseModel):
    access_token: str

class TokenPayload(BaseModel):
    mobile: str
    role: Literal["admin", "recorder", "reviewer"]

