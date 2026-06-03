import csv
import os

from pyfzf.pyfzf import FzfPrompt
from rich import print

ALL_PROJECTS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "all-projects.csv")


def findAllProject():
    if not os.path.exists(ALL_PROJECTS_FILE):
        print("[red]all-projects.csv not found. Run option 9 first to generate it.")
        return

    with open(ALL_PROJECTS_FILE, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

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
