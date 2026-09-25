import os

from rich import print
from rich.console import Console

from py_libs.FilesHandle import FilesHandle
from py_libs.InputValidator import InputValidator
from py_libs.Print import Print
from py_libs.Rsync import Rsync

from modules.notifySend import notify_send
from modules.pushFiles import _build_remote_path, _select_project

console = Console()


def _select_local_destination():
    cwd = os.getcwd()
    console.print(f"\n[cyan]Current directory:[/cyan] {cwd}")

    if InputValidator.confirm("Download into current directory?"):
        return cwd

    path = InputValidator.get_string("Enter full local destination path: ")
    return FilesHandle().ensure_dir(path)


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
    delete = use_delete == "y"

    console.print(f"\n[green]Remote:[/green] {USERNAME}@{HOST}:{source}")
    console.print(f"[green]Local:[/green]  {local_dest}")

    confirm = input("\nProceed? (y/n): ").strip().lower()
    if confirm != "y":
        Print.warning("Cancelled")
        return

    Rsync.pull(
        source,
        local_dest,
        user=USERNAME,
        host=HOST,
        password=PASSWORD,
        port=PORT,
        delete=delete,
    )
    notify_send(f"Pulled {HOST}:{source} → {local_dest}")
    Print.success(f"Done: {HOST}:{source} → {local_dest}")
