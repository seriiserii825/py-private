import os
import subprocess

from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from classes.utils.Select import Select
from libs.buffer import addToClipBoard
from modules.notifySend import notify_send
from utils.getVps import getVps


def server():
    choosed_server = serverMenu()
    print(Panel(f"Choosed server: [green]{choosed_server['name']}"))
    password = choosed_server["password"]
    port = choosed_server["port"]
    addToClipBoard(password)
    notify_send("Server password copied to clipboard 📋")
    user = choosed_server["user"]
    vps = choosed_server
    ip = vps["ip"]

    cmd = [
        "sshpass", "-p", password,
        "ssh", "-t", "-p", str(port),
        f'{user}@{ip}',
    ]
    subprocess.run(cmd)  # noqa: F821
    # command = f"ssh -p {port} {choosed_server['user']}@{choosed_server['ip']}"
    # print(Panel(f"Command: [green]{command}"))
    # os.system(command)


def serverMenu():
    vps_list = getVps()
    # print(f"vps_list: {vps_list}")
    server_names = [vps["name"] for vps in vps_list]
    # print(f"server_names: {server_names}")
    choice = Select.select_with_fzf(server_names + ["Exit"])
    # print(f"choice: {choice}")
    if choice[0] == "Exit":
        print("[blue]Goodbye, have a nice day! 👋")
        exit()
    index = server_names.index(choice[0])
    if index < 0 or index >= len(server_names):
        print(Panel("[red]Invalid index"))
        serverMenu()
    return vps_list[index]
