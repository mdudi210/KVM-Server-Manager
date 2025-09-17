from fastapi import APIRouter, HTTPException, Depends
from backend.src.utils.ssh import ssh_client, execute_ssh_command
from backend.src.schema.schema import ChangeState, State
from backend.src.auth.user_auth import verify_user
from backend.config.logging_setting import setup_logger

router = APIRouter()
logger = setup_logger("vm state endpoint")

@router.post("/vm/state/")
def change_state(data: ChangeState, claims = Depends(verify_user)):
    client = ssh_client()

    if data.state not in State.__members__:
        logger.error(f"Entered the state of VM")
        raise HTTPException(status_code=400, detail="invalid state type")
    
    command = f"sudo virsh {data.state} {data.name}"

    try:
        output, error = execute_ssh_command(client, command)

        if error:
            logger.error(f"{claims.get("sub")} got {error} when changing state of vm {data.name} to {data.state}")
            raise HTTPException(status_code=500, detail=error)
        
        logger.info(f"{claims.get("sub")} change state of vm {data.name} to {data.state}")
        return {
            "Message" : "",
            "Body" : {
                "output" : output.strip().split()[-1]
            }
        }

    except HTTPException as e:
        logger.exception("HTTP Unexpected error during VM creation")
        raise HTTPException(status_code=520, detail=f"{e}")
    except Exception as e:
        logger.exception("Unexpected error during VM creation")
        raise HTTPException(status_code=500, detail=f"{e}")
    finally:
        client.close()