import os
import subprocess

from rich import print
from rich.console import Console

from modules.notifySend import notify_send
from modules.pushFiles import _ask_remote_path, _select_server

console = Console()

DOWNLOADS_DIR = os.path.expanduser("~/Downloads")


def downloadFromServer():
    print("[bold blue]Download from server via rsync[/bold blue]")

    print("\n[cyan]Select server:[/cyan]")
    vps = _select_server()
    if vps is None:
        return

    HOST = vps["ip"]
    PORT = vps["port"]
    USERNAME = vps["user"]
    PASSWORD = vps["password"]

    print(
        "\n[yellow]Add / at the end of the path for a folder, "
        "omit it for a single file[/yellow]"
    )
    remote_path = _ask_remote_path()
    if remote_path is None:
        return

    kind = "folder" if remote_path.endswith("/") else "file"
    # rsync treats a trailing "/" on the source as "sync contents only";
    # strip it so the folder itself is copied into Downloads instead of
    # its contents being merged loose into the destination.
    source_path = remote_path.rstrip("/") if kind == "folder" else remote_path

    os.makedirs(DOWNLOADS_DIR, exist_ok=True)

    console.print(
        f"\n[green]Remote ({kind}):[/green] {USERNAME}@{HOST}:{remote_path}"
    )
    console.print(f"[green]Local:[/green]  {DOWNLOADS_DIR}")

    confirm = input("\nProceed? (y/n): ").strip().lower()
    if confirm != "y":
        print("[yellow]Cancelled")
        return

    command = [
        "sshpass", "-p", PASSWORD,
        "rsync", "-av", "--progress",
        f"--rsh=sshpass -p {PASSWORD} ssh -p {PORT}",
        f"{USERNAME}@{HOST}:{source_path}",
        DOWNLOADS_DIR + "/",
    ]

    print(f"\n[dim]{' '.join(str(c) for c in command)}[/dim]\n")
    subprocess.run(command, check=True)
    notify_send(f"Downloaded {HOST}:{remote_path} → {DOWNLOADS_DIR}")
    print(f"[green]Done: {HOST}:{remote_path} → {DOWNLOADS_DIR}")
