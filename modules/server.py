import os
from libs.buffer import addToClipBoard
from utils.getVps import getVps
from termcolor import colored
from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.table import Table

def server():
    choosed_server = serverMenu()
    print(Panel(f"Choosed server: [green]{choosed_server['name']}"))
    password = choosed_server['password']
    port = choosed_server['port']
    addToClipBoard(password)
    command = f"ssh -p {port} {choosed_server['user']}@{choosed_server['ip']}"
    # command = f"sshpass -p {password} ssh -p {port} {choosed_server['user']}@{choosed_server['ip']}"
    # command = f"sshpass -p {password} ssh {choosed_server['user']}@{choosed_server['ip']}"
    print(Panel(f"Command: [green]{command}"))
    os.system(command)

def serverMenu():
    vps_list = getVps()
    server_names = [vps['name'] for vps in vps_list]
    print(Panel("[blue]Choose a server by index"))
    table = Table(title="Choose a server")
    table.add_column("Index", style="magenta")
    table.add_column("Server", justify="right", style="cyan", no_wrap=True)
    for i, server_name in enumerate(server_names):
        table.add_row(str(i), server_name)
    console = Console()
    console.print(table)
    index = int(input("Enter the index: "))
    print(Panel(f"Index: [green]{index}"))
    if index < 0 or index >= len(server_names):
        print(Panel(f"[red]Invalid index"))
        serverMenu()
    return vps_list[index]

