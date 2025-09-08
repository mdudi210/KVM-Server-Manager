from fastapi import APIRouter, HTTPException, Depends
from backend.src.utils.ssh import ssh_client
from backend.src.schema.schema import NewVmRequest
from backend.src.auth.admin_auth import verify_admin
from backend.config.logging_setting import setup_logger
import paramiko
import shlex
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
logger = setup_logger("vm_new")

LINUX_ISO = os.getenv("LINUX_ISO")
WIN_ISO = os.getenv("WIN_ISO")


def execute_ssh_command(client: paramiko.SSHClient, command: str) -> tuple[str, str]:
    """Execute a command on SSH client and return output, error."""
    try:
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        return output, error
    except Exception:
        logger.exception(f"SSH command failed: {command}")
        raise HTTPException(status_code=500, detail="SSH command execution failed")


@router.post("/vm/new")
def create_new_vm(data: NewVmRequest, claims=Depends(verify_admin)):
    """
    Create a new VM (Linux or Windows) using virt-install.
    """
    client = ssh_client()
    if isinstance(client, str):  # ssh_client returned error string
        logger.error(f"SSH connection failed: {client}")
        raise HTTPException(status_code=500, detail="SSH connection failed")

    # Sanitize VM name to avoid command injection
    safe_vm_name = shlex.quote(data.name)

    if data.vmtoinstall == "Linux":
        command = (
            f"sudo virt-install --name {safe_vm_name} --memory 2534 --vcpus 2 "
            f"--cpu host-passthrough --os-variant centos-stream9 "
            f"--disk path=/home/{safe_vm_name}.qcow2,size=50,format=qcow2,bus=virtio "
            f"--cdrom {LINUX_ISO} "
            f"--network network=default,model=virtio --graphics vnc,listen=127.0.0.1 "
            f"--video virtio --channel unix,target_type=virtio,name=org.qemu.guest_agent.0 "
            f"--boot cdrom,hd --controller type=sata --features acpi=on,apic=on "
            f"--noautoconsole"
        )
    elif data.vmtoinstall == "Windows":
        command = (
            f"sudo virt-install --name {safe_vm_name} --memory 5192 --vcpus 2 "
            f"--cpu host-passthrough --os-variant win11 "
            f"--disk path=/home/{safe_vm_name}.qcow2,size=50,format=qcow2,bus=sata "
            f"--cdrom {WIN_ISO} "
            f"--network network=default,model=e1000e --graphics vnc --video bochs "
            f"--boot hd --controller type=sata --features acpi=on,apic=on "
            f"--noautoconsole"
        )
    else:
        logger.warning(f"Invalid VM type entered: {data.vmtoinstall}")
        raise HTTPException(status_code=400, detail="Invalid VM Type")

    try:
        output, error = execute_ssh_command(client, command)

        if error:
            logger.error(
                f"{claims.get('sub')} encountered error while creating {data.vmtoinstall} VM '{data.name}': {error}"
            )
            raise HTTPException(status_code=500, detail=error)

        logger.info(
            f"{claims.get('sub')} created {data.vmtoinstall} VM successfully: {data.name}"
        )
        return {
            "Message": f"{data.vmtoinstall} VM created successfully",
            "Body": {"output": output},
        }

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error during VM creation")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        client.close()
