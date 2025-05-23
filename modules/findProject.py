from rich.console import Console
from rich.table import Table
from utils.getProjectsFromCsv import getProjectsFromCsv

def findProject():
    project_name = input("Enter the project name: ")
    projects = getProjectsFromCsv()
    found_projects = [project for project in projects if project_name.lower() in project['title'].lower()]
    if len(found_projects) > 0:
        table = Table(title="Found Projects")
        table.add_column("Title", style="magenta")
        table.add_column("VPS", style="green")
        table.add_column("Path", style="blue")
        for project in found_projects:
            table.add_row(project['title'], project['vps'], project['path'])
        console = Console()
        console.print(table)
    else:
        print(f"No projects found with the name '{project_name}'.")
