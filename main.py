#!/usr/bin/python3

from modules.backups import backups
from modules.connectToProject import connectToProject
from modules.server import server
from rich import print
from rich.console import Console
from rich.table import Table

from modules.uploadFiles import uploadFiles
from modules.viewProjects import viewProjects

if __name__ == "__main__":
    print("[green]Start script")

def menu():
    table = Table(title="Choose an option")
    table.add_column("Index", style="magenta")
    table.add_column("Option", no_wrap=True)
    table.add_row("1", "[green]View All Projects")
    table.add_row("2", "[blue]Upload Backup")
    table.add_row("3", "[yellow]Connect to Server")
    table.add_row("4", "[yellow]Connect to project on server")
    table.add_row("5", "[blue]Upload files")
    table.add_row("6", "[exit]Exit")
    console = Console()
    console.print(table)

    input_user = input("Enter your choice: ")
    if input_user == "1":
        viewProjects()
        menu()
    elif input_user == "2":
        backups()
        menu()
    elif input_user == "3":
        server()
        menu()
    elif input_user == "4":
        connectToProject()
        menu()
    elif input_user == "5":
        uploadFiles()
        menu()
    elif input_user == "6":
        print("[red]Exit")
        exit()
    else:
        print("[red]Invalid choice")
        exit()
menu()
