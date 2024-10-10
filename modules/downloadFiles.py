import subprocess
import pyperclip
from rich import print

from libs.buffer import addToClipBoardFile
from modules.getHostByProjectName import getHostByProjectName
from modules.getServerByHost import getServerByHost
from modules.notifySend import notify_send
def downloadFiles():
    clipboard = pyperclip.paste()
    print(f"clipboard: {clipboard}")
    if clipboard.startswith("/home/"):
        conting_segments = clipboard.split("/")
        if len(conting_segments) >= 7:
            project_name = conting_segments[8]
            print(f"Project name: {project_name}")
            host_name = getHostByProjectName(project_name)
            if host_name is None:
                print("[red]Project not found")
                exit()
            server = getServerByHost(host_name)
            print(f"server: {server}")
            if server is None:
                print("[red]Server not found")
                exit()
            host= server[1]
            ip = server[2]
            password = server[3].split("\n")[0]
            # addToClipBoardFile(password)
            # Constructing the command
            command = f"sshpass -p {password} scp -r {host}@{ip}:{clipboard} ."

            # Running the command
            try:
                subprocess.run(command, shell=True, check=True)
                message = f"File {clipboard} transfer completed successfully."
                print(message)
                notify_send(message)
            except subprocess.CalledProcessError as e:
                print(f"Error during SCP transfer: {e}")
    else:
        print("[red]Invalid path, go to server and copy path of the file to clipboard")
        exit()

