import uuid
from src.utils.hash_password import hash_password
from src.utils.db_connection import OpenDb

try:
    with OpenDb() as cursor:
        # create roles table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            id CHAR(36) PRIMARY KEY,
            role VARCHAR(50) NOT NULL UNIQUE
        );
        """)

        # create users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id CHAR(36) PRIMARY KEY,
            username VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(128) NOT NULL,
            role_id CHAR(36),
            FOREIGN KEY (role_id) REFERENCES roles(id)
        );
        """)

        # insert default roles
        cursor.execute("INSERT INTO roles (id,role) VALUES (%s,%s)", (str(uuid.uuid4()),'admin'))
        cursor.execute("INSERT INTO roles (id,role) VALUES (%s,%s)", (str(uuid.uuid4()),'user'))

        # fetch role IDs
        cursor.execute("SELECT id FROM roles WHERE role='admin'")
        admin_role_id = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM roles WHERE role='user'")
        user_role_id = cursor.fetchone()[0]

        # hash password with SHA-512
        hashed_password = hash_password("password123")

        # insert default users
        cursor.execute("""
        INSERT INTO users (id, username, password, role_id)
        VALUES (%s, %s, %s, %s)
        """, (str(uuid.uuid4()), "admin", hashed_password, admin_role_id))

        cursor.execute("""
        INSERT INTO users (id, user, password, role_id)
        VALUES (%s, %s, %s, %s)
        """, (str(uuid.uuid4()), "testuser", hashed_password, user_role_id))

        print(f"Database created with default roles & users: ")

except Exception as e:
    print(f"Error: {e}")