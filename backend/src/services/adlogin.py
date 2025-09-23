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
        result = authenticate_with_ad(data.username, data.password)
        if not result[0]:
            logger.warning(f"Failed AD login attempt for username: {data.username}")
            raise HTTPException(status_code=401, detail="Invalid AD credentials")

        try:
            access_token = Authorize.create_access_token(
                subject=data.username,
                expires_time=timedelta(days=7),
                user_claims={
                    "id": result[2],
                    "role" : result[1]
                }
            )
        except Exception as jwt_error:
            logger.exception("Error while generating JWT token")
            raise HTTPException(status_code=500, detail="Token generation failed")

        logger.info(f"User '{data.username}' logged in successfully via AD")
        return {
            "access_token": access_token,
            "id": result[2],
            "username": data.username,
            "role" : result[1]

        }

    except HTTPException as e:
        logger.exception("HTTP Unexpected error in login")
        raise  HTTPException(status_code=520, detail=f"{e}")
    except Exception as e:
        logger.exception("Unexpected error in login API")
        raise HTTPException(status_code=500, detail=str(e))
