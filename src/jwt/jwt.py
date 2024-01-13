from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import ExpiredSignatureError, JWTError, jwt
from starlette.status import HTTP_401_UNAUTHORIZED

from src.config import settings
from src.jwt.model import TokenPayload


def create_access_token(data: TokenPayload):
    to_encode = data.model_dump()

    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    return encoded_jwt

def decode_access_token(token: str) -> TokenPayload:
    if(token == None or token == ""):
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail={"message": "Invalid Token"})
    try:
        user = jwt.decode(token, settings.secret_key, settings.algorithm)
        return TokenPayload(**user)

    except ExpiredSignatureError:
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail={"message": "Token Expired"})
    except JWTError:
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail={"message": "Invalid Token"})



