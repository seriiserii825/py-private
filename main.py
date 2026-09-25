#!/usr/bin/python3

import os
import sys

from py_libs.Print import Print
from py_libs.Select import Select

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


MENU_ITEMS = [
    ("View All Projects", viewProjects, True),
    ("Find Project", findProject, True),
    ("Upload Backup", backups, True),
    ("Connect to Server", server, True),
    ("Connect to project on server", connectToProject, True),
    ("Upload files", uploadFiles, True),
    ("Download files", downloadFiles, True),
    ("Copy server data to clipboard", copyServerDataToClipboard, False),
    ("All projects to file", allProjectsToFile, True),
    ("Find in all projects", findAllProject, True),
    ("Push files/folder to project or server (rsync)", pushFiles, True),
    ("Recent modified files on server", recentFiles, True),
    ("Pull files/folder from project (rsync)", pullFiles, True),
    ("Download from server (rsync)", downloadFromServer, True),
]

EXIT_LABEL = "Exit"


def menu():
    labels = [label for label, _, _ in MENU_ITEMS] + [EXIT_LABEL]
    choice = Select.select_fzf_one(labels)

    if choice is None or choice == EXIT_LABEL:
        Print.error("Exit")
        exit()

    for label, action, loop_back in MENU_ITEMS:
        if choice == label:
            action()
            if loop_back:
                menu()
            exit()


checkCsvFiles()
menu()
