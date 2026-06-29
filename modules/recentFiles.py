import subprocess
import sys

from rich import print
from rich.console import Console
from rich.table import Table

from libs.selectWithFzf import selectWithFzf
from modules.Projects import Projects
from utils.getProjectsFromCsv import getProjectsFromCsv

console = Console()

_NAV = ["--- back to menu ---", "--- exit ---"]

SEARCH_DIRS = [
    "uploads",
    "wp-content",
    "public_html",
    "custom",
]


def _fzf(items):
    result = selectWithFzf(list(items) + _NAV)
    if result == "--- back to menu ---":
        return None
    if result == "--- exit ---":
        sys.exit(0)
    return result


def _select_project():
    projects = getProjectsFromCsv()
    names = [p["title"] for p in projects]
    selected_name = _fzf(names)
    if selected_name is None:
        return None

    p = Projects()
    p.project_name = selected_name
    p.getProjectFromCsv()
    p.getServerFromCsv()
    return p


def recentFiles():
    print("[bold blue]Recently modified files on server[/bold blue]")

    print("\n[cyan]Select project:[/cyan]")
    project = _select_project()
    if project is None:
        return

    HOST = project.project["server_host"]
    PORT = project.project["server_port"]
    USERNAME = project.project["server_login"]
    PASSWORD = project.project["server_password"]
    BASE_PATH = project.project["server_path"]

    # Strip trailing slash, ensure we have public_html base
    if "public_html" in BASE_PATH:
        public_html = BASE_PATH.split("public_html")[0] + "public_html"
    else:
        public_html = BASE_PATH.rstrip("/")

    dir_choice = _fzf(SEARCH_DIRS)
    if dir_choice is None:
        return

    if dir_choice == "custom":
        custom = input("Enter path relative to public_html (e.g. wp-content/themes/my-theme): ").strip().lstrip("/")
        search_path = f"{public_html}/{custom}"
    elif dir_choice == "public_html":
        search_path = public_html
    else:
        search_path = f"{public_html}/{dir_choice}"

    minutes_input = input("Show files modified in last N minutes (default 5): ").strip()
    minutes = minutes_input if minutes_input.isdigit() else "5"

    console.print(f"\n[cyan]Searching:[/cyan] {search_path}")
    console.print(f"[cyan]Modified in last:[/cyan] {minutes} min\n")

    find_cmd = (
        f"find {search_path} -type f -cmin -{minutes} "
        f"-printf '%CY-%Cm-%Cd %CH:%CM  %p\\n' 2>/dev/null | sort -r"
    )

    result = subprocess.run(
        ["sshpass", "-p", PASSWORD, "ssh", "-p", str(PORT),
         f"{USERNAME}@{HOST}", find_cmd],
        capture_output=True, text=True
    )

    lines = [l for l in result.stdout.strip().splitlines() if l]

    if not lines:
        print(f"[yellow]No files modified in the last {minutes} minutes.")
        return

    table = Table(title=f"Modified in last {minutes} min — {HOST}:{search_path}")
    table.add_column("Date & Time", style="cyan", no_wrap=True)
    table.add_column("Path", style="green")

    for line in lines:
        parts = line.split("  ", 1)
        if len(parts) == 2:
            table.add_row(parts[0].strip(), parts[1].strip())
        else:
            table.add_row("", line)

    console.print(table)
    print(f"\n[dim]Total: {len(lines)} file(s)[/dim]")
