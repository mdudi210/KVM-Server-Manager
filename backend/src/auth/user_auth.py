from fastapi import Depends, HTTPException
from backend.src.schema.schema import Roles
from fastapi_jwt_auth import AuthJWT
from backend.src.utils.user_exists import user_exists
from backend.src.utils.ad_user_exists import ad_user_exists


def verify_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        claims = Authorize.get_raw_jwt()
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid or missing token: {str(e)}")

    role = claims.get('role')
    if not role:
        raise HTTPException(status_code=400, detail="Missing role in token claims")

    try:
        if not role or role not in Roles.__members__:
            raise HTTPException(status_code=403, detail="User access required")

        user_id = claims.get("id")
        if not user_id:
            raise HTTPException(status_code=400, detail="Missing user id in token claims")
        # if not user_exists(user_id):
        # if not ad_user_exists(user_id):
        #     raise HTTPException(status_code=400, detail="User does not exist")

        return claims
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error during user verification: {str(e)}")
