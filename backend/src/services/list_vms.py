from fastapi import APIRouter, HTTPException, Depends
from backend.src.utils.ssh import ssh_client
from backend.src.auth.user_auth import verify_user
from backend.config.logging_setting import setup_logger
from backend.src.utils.parse_vm_status import parse_vm_status

router = APIRouter()

@router.get("/vms")
def list_all_vm(claims = Depends(verify_user)):
    logger = setup_logger("main")
    client = ssh_client()
    command_to_execute = "virsh list --all"

    stdin, stdout, stderr = client.exec_command(command_to_execute)
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    if output:
        logger.info(f"{claims.get("sub")} listed all VM")
        return {
            "Message" : "",
            "Body" : {
                "output" : parse_vm_status(output)
            }
        }
    if error:
        logger.error(f"{claims.get("sub")} got {error} when listing all VM")
        return {
            "Message" : "",
            "Body" : {
                "output" : error
            }
        }