import os
from rich import print
from pathlib import Path


class Projects:
    def __init__(self):
        self.project = {
                "name": "",
                "server_name": "",
                "server_host": "",
                "server_path": "",
                "server_login": "",
                "server_password": "",
                "server_port": 22
                }
        self.project_name = ""
        current_file = Path(__file__).resolve()
        self.SCRIPT_DIR = current_file.parents[1]

    def getProjects(self):
        return self.project

    def isCurrentProject(self):
        current_dir = os.getcwd()
        self.project_name = current_dir.split("/")[-1]
        self.getProjectFromCsv()
        self.getServerFromCsv()

    def getProjectFromCsv(self):
        csv_file = f"{self.SCRIPT_DIR}/list.csv"
        with open(csv_file, "r") as f:
            for line in f:
                project_data = line.strip().split(",")
                if project_data[0] == self.project_name:
                    self.project['name'] = project_data[0]
                    self.project['server_name'] = project_data[1]
                    self.project['server_path'] = project_data[2]
        if not self.project:
            print("Project not found")
            exit()
        elif self.project['name'] != self.project_name:
            print("Project not found")
            exit()
        else:
            print(f"Project found: [green]{self.project['name']}")
            return self.project
    def getServerFromCsv(self):
        csv_file = f"{self.SCRIPT_DIR}/servers.csv"
        with open(csv_file, "r") as f:
            for line in f:
                server_data = line.strip().split(",")
                if server_data[0] == self.project['server_name']:
                    self.project['server_login'] = server_data[1]
                    self.project['server_host'] = server_data[2]
                    self.project['server_password'] = server_data[3]
                    # Check if server_data has at least 5 elements
                    if len(server_data) > 4 and server_data[4]:
                        self.project['server_port'] = server_data[4]
                    else:
                        self.project['server_port'] = 22
                    print(f"Server found: [green]{self.project['server_name']}")
        if not self.project['server_login']:
            print("[red]Server not found")
            exit()
