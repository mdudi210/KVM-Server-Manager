from fastapi import APIRouter, Depends, Response
from fastapi_jwt_auth import AuthJWT

from backend.src.schema.schema import LoginRequest
from backend.src.services.login import login as unified_login

router = APIRouter()


@router.post("/adlogin", deprecated=True)
def ad_login(data: LoginRequest, response: Response, Authorize: AuthJWT = Depends()):
    # Compatibility route; login flow is now fully unified in /login.
    return unified_login(data, response, Authorize)
