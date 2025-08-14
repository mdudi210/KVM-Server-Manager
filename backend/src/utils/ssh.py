import paramiko

# Server details
hostname = "10.168.12.142"
username = "root"
password = "Adm1n0n7y"
command_to_execute = "ls -l"

def ssh_client():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=hostname,username=username,password=password)
        return client
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your username and password.")
        return "Authentication failed. Please check your username and password."
    except paramiko.SSHException as e:
        print(f"SSH connection error: {e}")
        return f"SSH connection error: {e}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"An unexpected error occurred: {e}"