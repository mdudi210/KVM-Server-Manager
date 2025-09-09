from backend.src.utils.db_connection import OpenDb
from fastapi import HTTPException
from backend.config.logging_setting import setup_logger
import psycopg2

logger = setup_logger("register endpoint")

def user_exists(id: str) -> bool:
    try:
        with OpenDb() as cursor:
            cursor.execute(
                "SELECT username FROM users WHERE id=%s", (id,)
            )
            return cursor.fetchone() is not None
    except psycopg2.errors.UniqueViolation:  
        logger.warning(f"Duplicate username attempt: {username}")
        raise HTTPException(status_code=400, detail="User with this name already exists")
    except HTTPException:
        raise HTTPException(status_code=520, detail="Unknown Error")
    except Exception as e:
        logger.exception(f"Unexpected error while creating user '{username}'")
        raise HTTPException(status_code=500, detail="Internal Server Error")