import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def getHostByProjectName(project_name):
    file_path = os.path.join(ROOT_DIR, "list.csv")
    with open(file_path, "r") as file:
        for line in file:
            if project_name in line:
                return line.split(",")[1].strip()
    return None
