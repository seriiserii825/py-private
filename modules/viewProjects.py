from rich.console import Console
from rich.table import Table

from utils.getProjectsFromCsv import getProjectsFromCsv


def viewProjects():
    table = Table(title="Projects")
    table.add_column("Title", style="magenta")
    table.add_column("VPS", style="green")
    table.add_column("Path", style="blue")
    projects = getProjectsFromCsv()
    for project in projects:
        table.add_row(project["title"], project["vps"], project["path"])
    console = Console()
    console.print(table)
