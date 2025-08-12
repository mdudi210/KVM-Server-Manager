from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.src.utils.user_exists import user_exists

def verify_admin(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    claims = Authorize.get_raw_jwt()
    if claims.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    if not user_exists(claims.get("id")):
        raise HTTPException(status_code=400, detail="User does not exist")
    return claims