import os
import time
from pathlib import Path

from libs.buffer import addToClipBoard
from py_libs.CsvFile import CsvFile
from py_libs.Print import Print


class Projects:
    def __init__(self):
        self.project = {
            "name": "",
            "server_name": "",
            "server_host": "",
            "server_path": "",
            "server_login": "",
            "server_password": "",
            "server_port": 22,
        }
        self.project_name = ""
        current_file = Path(__file__).resolve()
        self.SCRIPT_DIR = current_file.parents[1]

    def getProjects(self):
        return self.project

    def getServerByName(self, server_name):
        csv_file = f"{self.SCRIPT_DIR}/servers.csv"
        rows = CsvFile(csv_file).read_csv() or []
        for row in rows:
            if row["name"] == server_name:
                return {
                    "name": row["name"],
                    "login": row["username"],
                    "host": row["ip"],
                    "password": row["password"],
                    "port": row["port"] if row.get("port") else 22,
                }
        return {}

    def copyServerToClipboard(self, server):
        addToClipBoard(f"{server['password']}")
        Print.success("Password copied to clipboard")
        time.sleep(3)  # Give user time to paste the password before overwriting
        if server["port"] == 22:
            addToClipBoard(f"ssh {server['login']}@{server['host']}")
        else:
            addToClipBoard(
                f"ssh -p {server['port']} {server['login']}@{server['host']}"
            )
        Print.success("User and host copied to clipboard")

    def isCurrentProject(self):
        current_dir = os.getcwd()
        self.project_name = current_dir.split("/")[-1]
        self.getProjectFromCsv()
        self.getServerFromCsv()

    def getProjectFromCsv(self):
        csv_file = f"{self.SCRIPT_DIR}/list.csv"
        rows = CsvFile(csv_file).read_csv() or []
        for row in rows:
            if row["title"] == self.project_name:
                self.project["name"] = row["title"]
                self.project["server_name"] = row["vps"]
                self.project["server_path"] = row["path"]
        if not self.project:
            Print.error("Project not found")
            exit()
        elif self.project["name"] != self.project_name:
            Print.error("Project not found")
            exit()
        else:
            Print.success(f"Project found: {self.project['name']}")
            return self.project

    def getServersFromCsv(self):
        csv_file = f"{self.SCRIPT_DIR}/servers.csv"
        rows = CsvFile(csv_file).read_csv() or []
        return [row["name"] for row in rows]

    def getServerFromCsv(self):
        csv_file = f"{self.SCRIPT_DIR}/servers.csv"
        rows = CsvFile(csv_file).read_csv() or []
        for row in rows:
            if row["name"] == self.project["server_name"]:
                self.project["server_login"] = row["username"]
                self.project["server_host"] = row["ip"]
                self.project["server_password"] = row["password"]
                self.project["server_port"] = (
                    row["port"] if row.get("port") else 22
                )
                Print.success(f"Server found: {self.project['server_name']}")
        if not self.project["server_login"]:
            Print.error("Server not found")
            exit()
