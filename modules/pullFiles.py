import os
import subprocess

from rich import print
from rich.console import Console

from modules.notifySend import notify_send
from modules.pushFiles import _build_remote_path, _select_project

console = Console()


def _select_local_destination():
    cwd = os.getcwd()
    console.print(f"\n[cyan]Current directory:[/cyan] {cwd}")

    use_default = input(
        "Download into current directory? (y/n, default y): "
    ).strip().lower()
    if use_default in ("", "y"):
        return cwd

    path = input("Enter full local destination path: ").strip()
    os.makedirs(path, exist_ok=True)
    return path


def pullFiles():
    print("[bold blue]Pull files from server via rsync[/bold blue]")

    print("\n[cyan]Select project:[/cyan]")
    project = _select_project()
    if project is None:
        return

    HOST = project.project["server_host"]
    PORT = project.project["server_port"]
    USERNAME = project.project["server_login"]
    PASSWORD = project.project["server_password"]
    BASE_PATH = project.project["server_path"]

    remote_path = _build_remote_path(BASE_PATH)
    if remote_path is None:
        return

    remote_name = os.path.basename(remote_path.rstrip("/"))
    sync_choice = input(
        f"Pull remote folder '{remote_name}' itself or its contents?\n"
        "  1) folder itself (creates subfolder locally)\n"
        "  2) contents only (merges into local destination)\n"
        "Choice (1/2, default 2): "
    ).strip()
    source = remote_path.rstrip("/") + ("" if sync_choice == "1" else "/")

    local_dest = _select_local_destination()
    if local_dest is None:
        return

    print(
        "\n[yellow]--delete:[/yellow] deletes local files removed on server\n"
        "Without --delete: local files are kept even if removed on server"
    )
    use_delete = input("Use --delete? (y/n, default n): ").strip().lower()
    delete_flag = ["--delete"] if use_delete == "y" else []

    console.print(f"\n[green]Remote:[/green] {USERNAME}@{HOST}:{source}")
    console.print(f"[green]Local:[/green]  {local_dest}")

    confirm = input("\nProceed? (y/n): ").strip().lower()
    if confirm != "y":
        print("[yellow]Cancelled")
        return

    command = [
        "sshpass", "-p", PASSWORD,
        "rsync", "-av", "--progress",
        f"--rsh=sshpass -p {PASSWORD} ssh -p {PORT}",
        *delete_flag,
        f"{USERNAME}@{HOST}:{source}",
        local_dest,
    ]

    print(f"\n[dim]{' '.join(str(c) for c in command)}[/dim]\n")
    subprocess.run(command, check=True)
    notify_send(f"Pulled {HOST}:{source} → {local_dest}")
    print(f"[green]Done: {HOST}:{source} → {local_dest}")
