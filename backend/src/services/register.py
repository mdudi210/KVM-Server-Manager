from fastapi import APIRouter, HTTPException, Depends
from backend.src.schema.schema import NewUser, Roles
from backend.src.utils.hash_password import hash_password
from backend.src.utils.db_connection import OpenDb
import uuid
from backend.src.auth.admin_auth import verify_admin
from backend.config.logging_setting import setup_logger
    
router = APIRouter()

@router.post("/register")
def register(data: NewUser, claims = Depends(verify_admin)):
    logger = setup_logger("main")
    user_id = uuid.uuid4()
    hashed_password = hash_password(data.password)
    username = data.username
    role = data.role
    if role not in Roles:
        raise HTTPException(status_code=400, detail="Invalid role type")
    try:
        with OpenDb() as cursor:
            cursor.execute(
                "SELECT id FROM roles WHERE role=%s", (role,),
            )
            role_id = cursor.fetchone()[0]
        with OpenDb() as cursor:
            cursor.execute(
                "INSERT INTO users (id, username, password, role_id) VALUES (%s,%s,%s,%s)", (str(user_id),str(username),str(hashed_password),role_id),
            )
    except Exception as e:
        logger.error(f"{claims.get("sub")} got {e} when creating for {username}")
        raise HTTPException(status_code=400, detail="Already have user with this name")
    logger.info(f"{claims.get("sub")} created Account for {username}")
    return {
        "Message" : f"Account created for {username} user"
    }