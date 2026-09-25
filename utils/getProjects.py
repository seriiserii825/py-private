import os

from termcolor import colored

from py_libs.CsvFile import CsvFile


def getProjects(theme_name):
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_file_path = os.path.join(ROOT_DIR, "list.csv")
    rows = CsvFile(csv_file_path).read_csv() or []
    projects = tuple(
        {"title": row["title"], "vps": row["vps"], "path": row["path"]}
        for row in rows
    )
    theme_is_in_projects = [
        project for project in projects if project["title"] == theme_name
    ]
    if not theme_is_in_projects:
        print(colored("Theme is not in projects", "red"))
        exit(1)
    else:
        return projects
