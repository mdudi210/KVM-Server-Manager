import ldap3
from ldap3.core.exceptions import LDAPException
from backend.src.schema.schema import Roles
from backend.config.logging_setting import setup_logger
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
logger = setup_logger("AD Auth")

ad_server = os.getenv("AD_SERVER")
ad_base_dn = os.getenv("AD_BASE_DN")

def authenticate_with_ad(username: str, password: str) -> list:
    try:
        server = ldap3.Server(ad_server, get_info=ldap3.ALL)
        
        with ldap3.Connection(
            server,
            user=username,
            password=password,
            auto_bind=True,
            check_names=True
        ) as conn:
            print("Authenticated:", conn.result["description"])
            search_filter = f"(sAMAccountName={username.split('@')[0]})"
            print(search_filter)
            conn.search(
                search_base=ad_base_dn,
                search_filter=search_filter,
                attributes=["KVMrole","objectGUID"] 
            )

            if not conn.entries:
                logger.warning(f"Attribute not found")
                raise HTTPException(status_code=400, detail="Attrinute not found")
            else:
                user_entry = conn.entries[0]
                role = user_entry.KVMrole.value
                if role not in Roles.__members__:
                    logger.warning(f"Invalid role '{role}'")
                    raise HTTPException(status_code=400, detail="Invalid role type")
                uid = user_entry.objectGUID.value

            return [True,role,uid]

    except LDAPException as e:
        logger.warning("Unable to connect to LDAP server:", e)
        raise HTTPException(status_code=400, detail="Incorrect username or password")
