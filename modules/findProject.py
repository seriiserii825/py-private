from py_libs.Menu import Menu

from utils.getProjectsFromCsv import getProjectsFromCsv


def findProject():
    project_name = input("Enter the project name: ")
    projects = getProjectsFromCsv()
    found_projects = [
        project
        for project in projects
        if project_name.lower() in project["title"].lower()
    ]
    if len(found_projects) > 0:
        rows = [
            [f"[magenta]{p['title']}", f"[green]{p['vps']}", f"[blue]{p['path']}"]
            for p in found_projects
        ]
        Menu.display("Found Projects", ["Title", "VPS", "Path"], rows)
    else:
        print(f"No projects found with the name '{project_name}'.")
