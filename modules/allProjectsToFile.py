import csv
import os
import subprocess

from rich import print
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from utils.getVps import getVps

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "all-projects.csv")


def allProjectsToFile():
    servers = getVps()
    rows = []
    console = Console()

    with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as progress:
        for srv in servers:
            task = progress.add_task(f"[cyan]{srv['name']}...", total=None)
            result = subprocess.run(
                [
                    "sshpass", "-p", srv["password"],
                    "ssh", "-p", str(srv["port"]),
                    "-o", "StrictHostKeyChecking=no",
                    "-o", "ConnectTimeout=10",
                    f"{srv['user']}@{srv['ip']}",
                    "ls ~/web",
                ],
                capture_output=True,
                text=True,
            )
            progress.remove_task(task)
            if result.returncode != 0:
                print(f"[red]  {srv['name']}: failed ({result.stderr.strip()})")
                continue
            projects = [line.strip() for line in result.stdout.splitlines() if line.strip()]
            for project in projects:
                rows.append({"server": srv["name"], "project": project})
            print(f"[green]  {srv['name']}: {len(projects)} projects")

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["server", "project"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n[bold green]Saved {len(rows)} projects to [white]{OUTPUT_FILE}")
