#!/usr/bin/python3

import os
import sys

from rich import print
from rich.console import Console
from rich.table import Table

from modules.allProjectsToFile import allProjectsToFile
from modules.findAllProject import findAllProject
from modules.backups import backups
from modules.connectToProject import connectToProject
from modules.copyServerDataToClipboard import copyServerDataToClipboard
from modules.downloadFiles import downloadFiles
from modules.findProject import findProject
from modules.server import server
from modules.pushFiles import pushFiles
from modules.recentFiles import recentFiles
from modules.uploadFiles import uploadFiles
from modules.viewProjects import viewProjects
from utils.checkCsvFiles import checkCsvFiles

if __name__ == "__main__":
    print("[green]Start script")


def menu():
    table = Table(title="Choose an option")
    table.add_column("Index", style="magenta")
    table.add_column("Option", no_wrap=True)
    table.add_row("1", "[green]View All Projects")
    table.add_row("1.1", "[green]Find Project")
    table.add_row("2", "[blue]Upload Backup")
    table.add_row("3", "[yellow]Connect to Server")
    table.add_row("4", "[yellow]Connect to project on server")
    table.add_row("5", "[blue]Upload files")
    table.add_row("6", "[green]Download files")
    table.add_row("7", "[blue]Copy server data to clipboard")
    table.add_row("9", "[cyan]All projects to file")
    table.add_row("9.1", "[cyan]Find in all projects")
    table.add_row("10", "[blue]Push files/folder to server (rsync)")
    table.add_row("11", "[cyan]Recent modified files on server")
    table.add_row("8", "[exit]Exit")
    console = Console()
    console.print(table)

    input_user = input("Enter your choice: ")
    if input_user == "1":
        viewProjects()
        menu()
    elif input_user == "1.1":
        findProject()
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
        downloadFiles()
        menu()
    elif input_user == "7":
        copyServerDataToClipboard()
        exit()
    elif input_user == "9":
        allProjectsToFile()
        menu()
    elif input_user == "9.1":
        findAllProject()
        menu()
    elif input_user == "10":
        pushFiles()
        menu()
    elif input_user == "11":
        recentFiles()
        menu()
    elif input_user == "8":
        print("[red]Exit")
        exit()
    else:
        print("[red]Invalid choice")
        exit()


checkCsvFiles()
menu()
