from fastapi import APIRouter, HTTPException, Depends
from backend.src.utils.ssh import ssh_client, execute_ssh_command
from backend.src.schema.schema import CloneRequest
from backend.src.auth.admin_auth import verify_admin
from backend.config.logging_setting import setup_logger
import shlex 
import os
from dotenv import load_dotenv

load_dotenv()

LINUX_TEMPLATE = os.getenv("LINUX_TEMPLATE")
WIN_TEMPLATE = os.getenv("WIN_TEMPLATE")

router = APIRouter()
logger = setup_logger("vm_clone")


@router.post("/vm/clone")
def create_clone(data: CloneRequest, claims=Depends(verify_admin)):
    client = ssh_client()
    if isinstance(client, str):
        logger.error(f"SSH connection failed: {client}")
        raise HTTPException(status_code=500, detail="SSH connection failed")

    safe_vm_name = shlex.quote(data.name)

    if data.vmtoinstall == "Linux":
        command = f"sudo virt-clone --original {LINUX_TEMPLATE} --name {safe_vm_name} --file /home/{safe_vm_name}.qcow2"
    elif data.vmtoinstall == "Windows":
        command = f"sudo virt-clone --original {WIN_TEMPLATE} --name {safe_vm_name} --file /home/{safe_vm_name}.qcow2"
    else:
        logger.warning(f"Invalid VM type entered: {data.vmtoinstall}")
        raise HTTPException(status_code=400, detail="Invalid VM Type")

    try:
        output, error = execute_ssh_command(client, command)

        if error:
            logger.error(
                f"{claims.get('sub')} encountered error while cloning {data.vmtoinstall} VM '{data.name}': {error}"
            )
            raise HTTPException(status_code=500, detail=error)

        logger.info(
            f"{claims.get('sub')} cloned {data.vmtoinstall} VM successfully: {data.name}"
        )
        return {
            "Message": f"{data.vmtoinstall} VM cloned successfully",
            "Body": {"output": output},
        }

    except HTTPException as e:
        logger.exception("HTTP Unexpected error during VM clone operation")
        raise HTTPException(status_code=520, detail=f"{e}")
    except Exception as e:
        logger.exception("Unexpected error during VM clone operation")
        raise HTTPException(status_code=500, detail=f"{e}")
    finally:
        client.close()
