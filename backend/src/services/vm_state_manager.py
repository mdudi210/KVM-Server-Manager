from fastapi import APIRouter, HTTPException, Depends
from backend.src.utils.ssh import ssh_client
from backend.src.schema.schema import ChangeState
from backend.src.auth.user_auth import verify_user
from backend.config.logging_setting import setup_logger


router = APIRouter()

@router.post("/vm/state/")
def change_state(data: ChangeState, claims = Depends(verify_user)):
    logger = setup_logger("main")
    client = ssh_client()
    command_to_execute = ""

    if data.state == "start":
        command_to_execute = f"sudo virsh {data.state} {data.name}"
    elif data.state == "shutdown":
        command_to_execute = f"sudo virsh {data.state} {data.name}"
    elif data.state == "destroy":
        command_to_execute = f"sudo virsh {data.state} {data.name}"
    elif data.state == "reboot":
        command_to_execute = f"sudo virsh {data.state} {data.name}"
    else:
        logger.error(f"Entered the state of VM")
        raise HTTPException(status_code=400, detail="invalid state type")

    stdin, stdout, stderr = client.exec_command(command_to_execute)
    # Read the output
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    if output:
        print("Command Output:")
        print(output)
        logger.info(f"{claims.get("sub")} change state of vm {data.name} to {data.state}")
        return {
            "Message" : "",
            "Body" : {
                "output" : output
            }
        }
    if error:
        print("Command Error:")
        print(error)
        logger.error(f"{claims.get("sub")} got {error} when changing state of vm {data.name} to {data.state}")
        return {
            "Message" : "",
            "Body" : {
                "output" : error
            }
        }