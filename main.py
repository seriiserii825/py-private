#!/usr/bin/python3

import os
import sys

from py_libs.Print import Print
from py_libs.Menu import Menu

from modules.allProjectsToFile import allProjectsToFile
from modules.findAllProject import findAllProject
from modules.backups import backups
from modules.connectToProject import connectToProject
from modules.copyServerDataToClipboard import copyServerDataToClipboard
from modules.downloadFiles import downloadFiles
from modules.downloadFromServer import downloadFromServer
from modules.findProject import findProject
from modules.findServerBySite import findServerBySite
from modules.server import server
from modules.pushFiles import pushFiles
from modules.pullFiles import pullFiles
from modules.recentFiles import recentFiles
from modules.uploadFiles import uploadFiles
from modules.viewProjects import viewProjects
from utils.checkCsvFiles import checkCsvFiles

if __name__ == "__main__":
    Print.success("Start script")


MENU_ITEMS = [
    # view / find
    ("View All Projects", viewProjects, True, "green"),
    ("Find Project", findProject, True, "green"),
    ("Find in all projects", findAllProject, True, "green"),
    ("Find server by site name (nmap)", findServerBySite, True, "green"),
    ("All projects to file", allProjectsToFile, True, "green"),
    # connect
    ("Connect to Server", server, True, "cyan"),
    ("Connect to project on server", connectToProject, True, "cyan"),
    ("Copy server data to clipboard", copyServerDataToClipboard, False, "cyan"),
    # upload / download
    ("Upload files", uploadFiles, True, "blue"),
    ("Download files", downloadFiles, True, "blue"),
    ("Upload Backup", backups, True, "blue"),
    # rsync
    (
        "Push files/folder to project or server (rsync)",
        pushFiles,
        True,
        "yellow",
    ),
    ("Pull files/folder from project (rsync)", pullFiles, True, "yellow"),
    ("Recent modified files on server", recentFiles, True, "yellow"),
    ("Download from server (rsync)", downloadFromServer, True, "yellow"),
]


def select_menu_option() -> int:
    labels = [f"[{color}]{label}" for label, _, _, color in MENU_ITEMS]
    return Menu.select_fzf_menu(labels) or 0


def menu():
    choice = select_menu_option()

    if choice == 0:
        Print.error("Exit")
        exit()

    _, action, loop_back, _ = MENU_ITEMS[choice - 1]
    action()
    if loop_back:
        menu()
    exit()


checkCsvFiles()
menu()
