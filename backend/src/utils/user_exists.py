from backend.src.utils.db_connection import OpenDb

def user_exists(id: str) -> bool:
    with OpenDb() as cursor:
        cursor.execute(
            "SELECT username FROM users WHERE id=%s", (id,)
        )
        return cursor.fetchone() is not None