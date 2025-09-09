from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from backend.src.schema.schema import LoginRequest
from backend.src.utils.hash_password import hash_password
from backend.src.utils.db_connection import OpenDb
from backend.config.logging_setting import setup_logger
from backend.config import JWT_auth_setting
from datetime import timedelta
import psycopg2

router = APIRouter()
logger = setup_logger("login endpoint")


@router.post("/login")
def login(data: LoginRequest, Authorize: AuthJWT = Depends()):
    try:
        hashed_password = hash_password(data.password)

        with OpenDb() as cursor:
            cursor.execute(
                "SELECT id, username, password, role_id FROM users WHERE username = %s",
                (data.username,)
            )
            result = cursor.fetchone()

        if not result or result[2] != hashed_password:
            logger.warning(f"Failed login attempt for username: {data.username}")
            raise HTTPException(status_code=401, detail="Invalid username or password")

        try:
            access_token = Authorize.create_access_token(
                subject=result[1],
                expires_time=timedelta(days=7),
                user_claims={
                    "id": result[0],
                    "role": result[3]
                }
            )
        except Exception as jwt_error:
            logger.exception("Error while generating JWT token")
            raise HTTPException(status_code=500, detail="Token generation failed")

        logger.info(f"User '{result[1]}' logged in successfully")
        return {
            "access_token": access_token,
            "id": result[0],
            "username": result[1],
            "role": result[3]
        }

    except psycopg2.Error as db_error:
        logger.exception("Database error occurred during login")
        raise HTTPException(status_code=500, detail="Database connection error")
    except HTTPException:
        raise  HTTPException(status_code=520, detail="Unknown Error")
    except Exception as e:
        logger.exception("Unexpected error in login API")
        raise HTTPException(status_code=500, detail="Internal Server Error")
