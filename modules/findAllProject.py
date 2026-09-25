import os

from pyfzf.pyfzf import FzfPrompt
from rich import print

from py_libs.CsvFile import CsvFile

ALL_PROJECTS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "all-projects.csv")


def findAllProject():
    if not os.path.exists(ALL_PROJECTS_FILE):
        print("[red]all-projects.csv not found. Run option 9 first to generate it.")
        return

    rows = CsvFile(ALL_PROJECTS_FILE).read_csv() or []

    if not rows:
        print("[yellow]all-projects.csv is empty.")
        return

    items = [f"{row['server']}  {row['project']}" for row in rows] + ["Exit"]

    fzf = FzfPrompt()
    try:
        selected = fzf.prompt(items)
    except Exception:
        return

    if not selected or selected[0] == "Exit":
        return

    parts = selected[0].split()
    print(f"\n[bold green]Server:[/] {parts[0]}  [bold green]Project:[/] {parts[-1]}")
