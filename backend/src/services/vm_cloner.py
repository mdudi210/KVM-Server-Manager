from fastapi import APIRouter, HTTPException, Depends
from backend.src.utils.ssh import ssh_client
from backend.src.schema.schema import CloneRequest
from backend.src.auth.admin_auth import verify_admin
from backend.config.logging_setting import setup_logger
import paramiko
import shlex  # for safe command argument escaping

router = APIRouter()
logger = setup_logger("vm_clone")


def execute_ssh_command(client: paramiko.SSHClient, command: str) -> tuple[str, str]:
    """
    Execute command over SSH and return output and error.
    """
    try:
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        return output, error
    except Exception as e:
        logger.exception(f"SSH command execution failed: {command}")
        raise HTTPException(status_code=500, detail="SSH command execution failed")


@router.post("/vm/clone")
def create_clone(data: CloneRequest, claims=Depends(verify_admin)):
    """
    Clone a new VM from a base template (Linux or Windows).
    """
    client = ssh_client()
    if isinstance(client, str):  # ssh_client returned error message
        logger.error(f"SSH connection failed: {client}")
        raise HTTPException(status_code=500, detail="SSH connection failed")

    # Sanitize VM name (to avoid command injection)
    safe_vm_name = shlex.quote(data.name)

    if data.vmtoinstall == "Linux":
        command = f"sudo virt-clone --original linux-template --name {safe_vm_name} --file /home/{safe_vm_name}.qcow2"
    elif data.vmtoinstall == "Windows":
        command = f"sudo virt-clone --original win-template --name {safe_vm_name} --file /home/{safe_vm_name}.qcow2"
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

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error during VM clone operation")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        client.close()
