#!/usr/bin/python3

import os
import sys

from py_libs.Menu import Menu
from py_libs.Print import Print

from modules.allProjectsToFile import allProjectsToFile
from modules.findAllProject import findAllProject
from modules.backups import backups
from modules.connectToProject import connectToProject
from modules.copyServerDataToClipboard import copyServerDataToClipboard
from modules.downloadFiles import downloadFiles
from modules.downloadFromServer import downloadFromServer
from modules.findProject import findProject
from modules.server import server
from modules.pushFiles import pushFiles
from modules.pullFiles import pullFiles
from modules.recentFiles import recentFiles
from modules.uploadFiles import uploadFiles
from modules.viewProjects import viewProjects
from utils.checkCsvFiles import checkCsvFiles

if __name__ == "__main__":
    Print.success("Start script")


def menu():
    columns = ["Index", "Option"]
    rows = [
        ["[magenta]1", "[green]View All Projects"],
        ["[magenta]1.1", "[green]Find Project"],
        ["[magenta]2", "[blue]Upload Backup"],
        ["[magenta]3", "[yellow]Connect to Server"],
        ["[magenta]4", "[yellow]Connect to project on server"],
        ["[magenta]5", "[blue]Upload files"],
        ["[magenta]6", "[green]Download files"],
        ["[magenta]7", "[blue]Copy server data to clipboard"],
        ["[magenta]9", "[cyan]All projects to file"],
        ["[magenta]9.1", "[cyan]Find in all projects"],
        ["[magenta]10", "[blue]Push files/folder to project or server (rsync)"],
        ["[magenta]11", "[cyan]Recent modified files on server"],
        ["[magenta]12", "[green]Pull files/folder from project (rsync)"],
        ["[magenta]13", "[green]Download from server (rsync)"],
        ["[magenta]8", "[exit]Exit"],
    ]
    Menu.display("Choose an option", columns, rows)

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
    elif input_user == "12":
        pullFiles()
        menu()
    elif input_user == "13":
        downloadFromServer()
        menu()
    elif input_user == "8":
        Print.error("Exit")
        exit()
    else:
        Print.error("Invalid choice")
        exit()


checkCsvFiles()
menu()
