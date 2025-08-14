from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

router = APIRouter()

# Config
SECRET_KEY = "super-secret-key"  # same as used to create token
ALGORITHM = "HS256"

security = HTTPBearer()

@router.get("/check-token")
def check_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
