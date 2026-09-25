import os

from py_libs.CsvFile import CsvFile

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def getHostByProjectName(project_name):
    file_path = os.path.join(ROOT_DIR, "list.csv")
    rows = CsvFile(file_path).read_csv() or []
    for row in rows:
        if project_name in row["title"]:
            return row["vps"]
    return None
