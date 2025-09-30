import ldap3
import uuid
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

def ad_user_exists(id: str) -> bool:
    try:
        server = ldap3.Server(ad_server, get_info=ldap3.ALL)

        clean_id = id.strip("{}")
        guid_obj = uuid.UUID(clean_id)
        le_bytes = guid_obj.bytes_le
        escaped = ''.join([f'\\{b:02X}' for b in le_bytes])
        print(escaped)
        search_filter = f"(objectGUID={escaped})"
        
        with ldap3.Connection(
            server,
            auto_bind=True,            
        ) as conn:
            conn.search(
                search_base=ad_base_dn,
                search_filter=search_filter,
                attributes=["cn"]
            )
            print(clean_id)
            print(conn)
            print(conn.entries)
            if not conn.entries:
                logger.warning(f"Attribute not found")
                raise HTTPException(status_code=403, detail="User diabled/removed in AD")
            return True

    except LDAPException as e:
        logger.warning("Unable to connect to LDAP server:", e)
        raise HTTPException(status_code=400, detail="Problem with AD server")