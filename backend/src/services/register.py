from fastapi import APIRouter, HTTPException, Depends
from backend.src.schema.schema import NewUser, Roles
from backend.src.utils.hash_password import hash_password
from backend.src.utils.db_connection import OpenDb
import uuid
from backend.src.auth.admin_auth import verify_admin
from backend.config.logging_setting import setup_logger
import psycopg2

router = APIRouter()
logger = setup_logger("register endpoint")


@router.post("/register")
def register(data: NewUser, claims=Depends(verify_admin)):
    user_id = str(uuid.uuid4())
    hashed_password = hash_password(data.password)
    username = data.username
    role = data.role

    # Validate role type
    if role not in Roles.__members__:  # safer check if Roles is Enum
        logger.warning(f"Invalid role '{role}' provided by {claims.get('sub')}")
        raise HTTPException(status_code=400, detail="Invalid role type")

    try:
        with OpenDb(commit=True) as cursor:  # auto-commit transaction
            # Fetch role ID
            cursor.execute("SELECT id FROM roles WHERE role = %s", (role,))
            role_record = cursor.fetchone()
            if not role_record:
                logger.warning(f"Role '{role}' not found in DB")
                raise HTTPException(status_code=400, detail="Role does not exist")
            role_id = role_record[0]

            # Insert new user
            cursor.execute(
                """
                INSERT INTO users (id, username, password, role_id) 
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, username, hashed_password, role_id),
            )

        logger.info(f"Admin {claims.get('sub')} created account for user '{username}'")
        return {"Message": f"Account created for {username}"}

    except psycopg2.errors.UniqueViolation:  # or mysql.connector.errors.IntegrityError
        logger.warning(f"Duplicate username attempt: {username}")
        raise HTTPException(status_code=400, detail="User with this name already exists")
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error while creating user '{username}'")
        raise HTTPException(status_code=500, detail="Internal Server Error")
