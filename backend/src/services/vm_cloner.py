from fastapi import APIRouter, HTTPException, Depends
from backend.src.utils.ssh import ssh_client
from backend.src.schema.schema import CloneRequest
from backend.src.auth.admin_auth import verify_admin
from backend.config.logging_setting import setup_logger


router = APIRouter()

@router.post("/vm/clone")
def create_clone(data : CloneRequest, claims = Depends(verify_admin)):
    logger = setup_logger("main")
    client = ssh_client()
    command_to_execute = ""

    if data.vmtoinstall == "Linux":
        command_to_execute = f"sudo virt-clone --original linux-template --name {data.name} --file /home/{data.name}.qcow2"
    elif data.vmtoinstall == "Windows":
        command_to_execute = f"sudo virt-clone --original windows-template --name {data.name} --file /home/{data.name}.qcow2"
    else:
        logger.error(f"Entered invalid vm type")
        raise HTTPException(status_code=400, detail="Invalid VM Type")

    
    stdin, stdout, stderr = client.exec_command(command_to_execute)
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    if output:
        print("Command Output:")
        print(output)
        logger.info(f"{claims.get("sub")} cloned {data.vmtoinstall} vm named {data.name}")
        return {
            "Message" : "",
            "Body" : {
                "output" : output
            }
        }
    if error:
        print("Command Error:")
        print(error)
        logger.error(f"{claims.get("sub")} got {error} when cloning {data.vmtoinstall} vm named {data.name}")
        return {
            "Message" : "",
            "Body" : {
                "output" : error
            }
        }