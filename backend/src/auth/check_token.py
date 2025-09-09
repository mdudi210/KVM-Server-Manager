from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

AUTHJWT_SECRET_KEY = os.getenv("AUTHJWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

security = HTTPBearer()

@router.get("/check-token")
def check_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, AUTHJWT_SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "valid": True,
            "expired": False,
            "payload": payload
        }
    except ExpiredSignatureError:
        return {
            "valid": False,
            "expired": True,
            "message": "Token expired"
        }
    except InvalidTokenError:
        return {
            "valid": False,
            "expired": None,
            "message": "Invalid token"
        }
