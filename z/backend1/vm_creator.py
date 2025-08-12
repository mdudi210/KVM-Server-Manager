from fastapi import APIRouter, HTTPException, Depends
from z.ssh import ssh_client
from schema.schema import NewVmRequest
from auth.auth import verify_admin
from logcode.logs import setup_logger

router = APIRouter()

@router.post("/vm/new")
def create_new_vm(data: NewVmRequest, claims = Depends(verify_admin)):
    logger = setup_logger("main")
    client = ssh_client()
    command_to_execute = ""

    if data.vmtoinstall == "Linux":
        command_to_execute = f"sudo virt-install --name {data.name} --memory 2534 --vcpus 2 --cpu host-passthrough --os-variant centos-stream9 --disk path=/home/{data.name}.qcow2,size=10,format=qcow2,bus=virtio --cdrom /var/lib/libvirt/iso/iso-share/CentOS-Stream-9-latest-x86_64-dvd1.iso --network network=default,model=virtio --graphics vnc,listen=127.0.0.1 --video virtio --channel unix,target_type=virtio,name=org.qemu.guest_agent.0 --boot cdrom,hd --controller type=sata --features acpi=on,apic=on --noautoconsole"
    elif data.vmtoinstall == "Windows":
        command_to_execute = f"sudo virt-install --name {data.name} --memory 5192 --vcpus 2 --cpu host-passthrough --os-variant win11 --disk path=/home/{data.name}.qcow2,size=15,format=qcow2,bus=sata --cdrom /var/lib/libvirt/iso/iso-share/Win11_22H2_English_x64v2.iso --network network=default,model=e1000e --graphics vnc --video bochs --boot hd --controller type=sata --features acpi=on,apic=on --noautoconsole"
    else:
        logger.error(f"Entered invalid vm type")
        raise HTTPException(status_code=400, detail="Invalid VM Type")

    
    stdin, stdout, stderr = client.exec_command(command_to_execute)
    
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    if output:
        print("Command Output:")
        print(output)
        logger.info(f"{claims.get("sub")} created {data.vmtoinstall} vm named {data.name}")
        return {
            "Message" : "",
            "Body" : {
                "output" : output
            }
        }
    if error:
        print("Command Error:")
        print(error)
        logger.error(f"{claims.get("sub")} got {error} when creating {data.vmtoinstall} vm named {data.name}")
        return {
            "Message" : "",
            "Body" : {
                "output" : error
            }
        }
