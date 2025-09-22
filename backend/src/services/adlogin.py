from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from backend.src.schema.schema import LoginRequest
from backend.src.utils.db_connection import OpenDb
from backend.src.utils.auth_ad import authenticate_with_ad
from backend.config.logging_setting import setup_logger
from datetime import timedelta

router = APIRouter()
logger = setup_logger("ADlogin endpoint")

@router.post("/adlogin")
def login(data: LoginRequest, Authorize: AuthJWT = Depends()):
    try:
        if not authenticate_with_ad(data.username, data.password):
            logger.warning(f"Failed AD login attempt for username: {data.username}")
            raise HTTPException(status_code=401, detail="Invalid AD credentials")

        with OpenDb() as cursor:
            cursor.execute(
                "SELECT id, role_id FROM users WHERE username = %s",
                (data.username,)
            )
            result = cursor.fetchone()

        if not result:
            logger.warning(f"User not found in DB: {data.username}")
            raise HTTPException(status_code=403, detail="User not authorized in system")

        user_id, role_id = result

        with OpenDb() as cursor:
            cursor.execute(
                "SELECT role FROM roles WHERE id = %s",
                (role_id,)
            )
            role = cursor.fetchone()[0]

        try:
            access_token = Authorize.create_access_token(
                subject=data.username,
                expires_time=timedelta(days=7),
                user_claims={
                    "id": user_id,
                    "role": role
                }
            )
        except Exception as jwt_error:
            logger.exception("Error while generating JWT token")
            raise HTTPException(status_code=500, detail="Token generation failed")

        logger.info(f"User '{data.username}' logged in successfully via AD")
        return {
            "access_token": access_token,
            "id": user_id,
            "username": data.username,
            "role": role
        }

    except HTTPException as e:
        logger.exception("HTTP Unexpected error in login")
        raise  HTTPException(status_code=520, detail=f"{e}")
    except Exception as e:
        logger.exception("Unexpected error in login API")
        raise HTTPException(status_code=500, detail=str(e))
