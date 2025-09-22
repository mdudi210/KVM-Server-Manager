import ldap3
from ldap3.core.exceptions import LDAPException
import os
from dotenv import load_dotenv

load_dotenv()

ad_server = os.getenv("AD_SERVER")

def authenticate_with_ad(username: str, password: str) -> bool:
    try:
        with ldap3.Connection(server=ad_server, user=username, password=password) as conn:
            print(conn.result["description"]) 
            return True
    except LDAPException:
        print('Unable to connect to LDAP server')
        return False