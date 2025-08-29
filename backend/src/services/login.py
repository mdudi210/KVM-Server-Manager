from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from backend.src.schema.schema import LoginRequest
from backend.src.utils.hash_password import hash_password
from backend.src.utils.db_connection import OpenDb
from backend.config.logging_setting import setup_logger
from backend.config import JWT_auth_setting
from datetime import timedelta
    
router = APIRouter()

@router.post("/login")
def login(data: LoginRequest, Authorize: AuthJWT = Depends()):
    logger = setup_logger("main")
    hashed_password = hash_password(data.password)
    with OpenDb() as cursor:
        cursor.execute(
            "SELECT id,username, password,role_id FROM users WHERE username=%s",(data.username,),
            )
        result = cursor.fetchone()

    if not result or result[2] != hashed_password:
        logger.error(f"{data.username} Entered wrong password")
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # JWT Payload (sub = subject is usually the username or email)
    access_token = Authorize.create_access_token(
        subject=result[1],  # username
        expires_time=timedelta(days=7),
        user_claims={"id": result[0], "role": result[3]}  # custom claims
    )

    logger.info(f"{result[1]} login")
    return {
        "access_token": access_token,
        "id": result[0],
        "username": result[1],
        "role": result[3]
    }