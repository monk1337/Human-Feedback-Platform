from pydantic import BaseModel

class User(BaseModel):
    mobile: str
    password: str
