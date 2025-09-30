from fastapi import HTTPException
from backend.config.logging_setting import setup_logger
import paramiko
import os
from dotenv import load_dotenv

load_dotenv()

# Server details
hostname = os.getenv("SSH_HOSTNAME")
username = os.getenv("SSH_USERNAME")
password = os.getenv("SSH_PASSWORD")

logger = setup_logger("ssh command")

def ssh_client():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=hostname,username=username,password=password)
        return client
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your username and password.")
        raise HTTPException(status_code=500, detail="Authentication failed. Please check your username and password.")
    except paramiko.SSHException as e:
        print(f"SSH connection error: {e}")
        raise HTTPException(status_code=500, detail=f"SSH connection error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")


def execute_ssh_command(client: paramiko.SSHClient, command: str) -> tuple[str, str]:
    try:
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        return output, error
    except Exception as e:
        logger.exception(f"SSH command execution failed: {command}")
        raise HTTPException(status_code=500, detail="SSH command execution failed")