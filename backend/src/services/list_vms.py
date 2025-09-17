from fastapi import APIRouter, HTTPException, Depends, Query
from backend.src.utils.ssh import ssh_client, execute_ssh_command
from backend.src.auth.user_auth import verify_user
from backend.config.logging_setting import setup_logger
from backend.src.utils.parse_vm_status import parse_vm_status
import paramiko

router = APIRouter()
logger = setup_logger("vm endpoint")


@router.get("/vm")
def list_all_vm(
    claims: dict = Depends(verify_user),
    vm_name: str | None = Query(default=None)
    ):

    client = ssh_client()
    if isinstance(client, str):  
        logger.error(f"SSH connection failed: {client}")
        raise HTTPException(status_code=500, detail="SSH connection failed")

    try:
        if vm_name:
            command = f"virsh domstate {vm_name}"
            output, error = execute_ssh_command(client, command)
        else:
            command = "virsh list --all"
            output, error = execute_ssh_command(client, command)
            if output:
                output = parse_vm_status(output)

        if error:
            logger.error(f"{claims.get('sub')} encountered error: {error}")
            raise HTTPException(status_code=500, detail=error)

        logger.info(f"{claims.get('sub')} retrieved VM info successfully")
        return {
            "Message": "VM info retrieved successfully",
            "Body": {
                "output": output
            }
        }

    except HTTPException as e:
        logger.exception("HTTP Unexpected error occurred while retrieving VM info")
        raise HTTPException(status_code=520, detail=f"{e}")
    except Exception as e:
        logger.exception("Unexpected error occurred while retrieving VM info")
        raise HTTPException(status_code=500, detail=f"{e}")
    finally:
        client.close()
