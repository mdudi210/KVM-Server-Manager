from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from psycopg2 import DatabaseError
from backend.src.utils.db_connection import OpenDb
from backend.src.utils.user_exists import user_exists

# def verify_user(Authorize: AuthJWT = Depends()):
#     Authorize.jwt_required()
#     claims = Authorize.get_raw_jwt()
#     role_id = claims.get('role')
#     with OpenDb() as cursor:
#         cursor.execute(
#             "SELECT role FROM roles WHERE id=%s",(role_id,),
#             )
#         role_name = cursor.fetchone()
#     if role_name[0] not in ["admin", "user"]:
#         raise HTTPException(status_code=403, detail="User access required")
#     if not user_exists(claims.get("id")):
#         raise HTTPException(status_code=400, detail="User does not exist")
#     return claims

def verify_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        claims = Authorize.get_raw_jwt()
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid or missing token: {str(e)}")

    try:
        role_id = claims.get('role')
        if not role_id:
            raise HTTPException(status_code=400, detail="Missing role in token claims")\
            
        with OpenDb() as cursor:
            cursor.execute("SELECT role FROM roles WHERE id=%s", (role_id,))
            role_name = cursor.fetchone()
    except DatabaseError as db_err:
        raise HTTPException(status_code=500, detail=f"Database error: {str(db_err)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error while verifying role: {str(e)}")

    try:
        if not role_name or role_name[0] not in ["admin", "user"]:
            raise HTTPException(status_code=403, detail="User access required")

        user_id = claims.get("id")
        if not user_id:
            raise HTTPException(status_code=400, detail="Missing user id in token claims")
        if not user_exists(user_id):
            raise HTTPException(status_code=400, detail="User does not exist")

        return claims
        
    except HTTPException:
        print("hello")
        raise HTTPException(status_code=500, detail=f"Unexpected error during user verification: {str(e)}")
        # re-raise HTTP exceptions directly
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error during user verification: {str(e)}")

