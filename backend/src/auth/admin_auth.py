from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.src.utils.db_connection import OpenDb
from backend.src.utils.user_exists import user_exists

def verify_admin(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    claims = Authorize.get_raw_jwt()
    role_id = claims.get('role')
    with OpenDb() as cursor:
        cursor.execute(
            "SELECT role FROM roles WHERE id=%s",(role_id,),
            )
        role_name = cursor.fetchone()
    if role_name[0] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    if not user_exists(claims.get("id")):
        raise HTTPException(status_code=400, detail="User does not exist")
    return claims