import time

from fastapi import APIRouter, Depends, HTTPException

from backend.config.logging_setting import setup_logger
from backend.src.auth.user_auth import verify_user
from backend.src.schema.schema import ChangeState, State
from backend.src.services.vm_events import (
    acquire_vm_lock,
    normalize_vm_state,
    publish_event,
    release_vm_lock,
)
from backend.src.utils.ssh import execute_ssh_command, ssh_client

router = APIRouter()
logger = setup_logger("vm_state_endpoint")

TARGET_STATES = {
    "start": "running",
    "shutdown": "shut off",
    "destroy": "shut off",
    "reboot": "running",
}

ALLOWED_CURRENT_STATES = {
    "start": {"shut off"},
    "shutdown": {"running"},
    "destroy": {"running"},
    "reboot": {"running"},
}


def _get_vm_state(client, vm_name: str) -> str:
    output, error = execute_ssh_command(client, f"virsh domstate {vm_name}")
    if error:
        raise HTTPException(status_code=500, detail=error)
    return normalize_vm_state(output)


def _wait_for_target_state(client, vm_name: str, target_state: str) -> str:
    for _ in range(12):
        current_state = _get_vm_state(client, vm_name)
        if current_state == target_state:
            return current_state
        time.sleep(2)
    return _get_vm_state(client, vm_name)


@router.post("/vm/state")
def change_state(data: ChangeState, claims=Depends(verify_user)):
    actor = claims.get("sub", "unknown")

    if data.state not in State.__members__:
        logger.error("Invalid VM state requested")
        raise HTTPException(status_code=400, detail="invalid state type")

    if not acquire_vm_lock(data.name):
        publish_event(
            {
                "event": "vm_operation_in_progress",
                "vm_name": data.name,
                "requested_by": actor,
            }
        )
        raise HTTPException(
            status_code=409,
            detail=f"Another operation is already in progress for VM '{data.name}'.",
        )

    client = ssh_client()

    try:
        current_state = _get_vm_state(client, data.name)

        if data.expected_state:
            expected_state = normalize_vm_state(data.expected_state)
            if expected_state != current_state:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "message": "VM state changed by another user.",
                        "vm_name": data.name,
                        "expected_state": expected_state,
                        "current_state": current_state,
                    },
                )

        if current_state not in ALLOWED_CURRENT_STATES[data.state]:
            raise HTTPException(
                status_code=409,
                detail={
                    "message": f"Cannot '{data.state}' VM from '{current_state}' state.",
                    "vm_name": data.name,
                    "current_state": current_state,
                },
            )

        command = f"sudo virsh {data.state} {data.name}"
        output, error = execute_ssh_command(client, command)

        if error:
            logger.error(
                "%s got %s when changing state of vm %s to %s",
                actor,
                error,
                data.name,
                data.state,
            )
            raise HTTPException(status_code=500, detail=error)

        target_state = TARGET_STATES[data.state]
        resulting_state = _wait_for_target_state(client, data.name, target_state)

        event_payload = {
            "event": "vm_state_changed",
            "vm_name": data.name,
            "requested_state": data.state,
            "previous_state": current_state,
            "current_state": resulting_state,
            "updated_by": actor,
        }
        publish_event(event_payload)

        logger.info(
            "%s changed VM '%s' from '%s' to '%s' via action '%s'",
            actor,
            data.name,
            current_state,
            resulting_state,
            data.state,
        )

        return {
            "Message": "VM state updated",
            "Body": {
                "vm_name": data.name,
                "requested_state": data.state,
                "previous_state": current_state,
                "current_state": resulting_state,
                "output": output.strip().split()[-1] if output else "",
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error during VM state change")
        raise HTTPException(status_code=500, detail=f"{e}")
    finally:
        release_vm_lock(data.name)
        client.close()
