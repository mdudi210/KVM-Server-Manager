import ldap3
from ldap3.core.exceptions import LDAPException
import os
from dotenv import load_dotenv

load_dotenv()

ad_server = os.getenv("AD_SERVER")
ad_base_dn = os.getenv("AD_BASE_DN")

def authenticate_with_ad(username: str, password: str) -> [bool,str,str]:
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
            
            if conn.entries:
                user_entry = conn.entries[0]
                print("Role:", user_entry.KVMrole.value)
                print("User ID:", user_entry.objectGUID.value)
            else:
                print("User not found in directory")
            
            return [True,user_entry.KVMrole.value,user_entry.objectGUID.value]

    except LDAPException as e:
        print("Unable to connect to LDAP server:", e)
        return [False,None,None]
