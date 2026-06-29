import os
import subprocess
import sys

from rich import print
from rich.console import Console

from libs.chooseDir import chooseDir
from libs.selectWithFzf import selectWithFzf
from modules.Projects import Projects
from modules.notifySend import notify_send
from utils.getProjectsFromCsv import getProjectsFromCsv

console = Console()

WP_SUBPATHS = [
    "public_html",
    "wp-content/themes",
    "wp-content/plugins",
    "wp-content/uploads",
    "wp-content",
    "custom",
]

_NAV = ["--- back to menu ---", "--- exit ---"]


def _fzf(items):
    """FZF with back/exit options. Returns None to go back, exits on exit."""
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

    selected = next(p for p in projects if p["title"] == selected_name)
    p = Projects()
    p.project_name = selected_name
    p.getProjectFromCsv()
    p.getServerFromCsv()
    return p


def _build_remote_path(base_path: str):
    console.print(f"\n[cyan]Base remote path:[/cyan] {base_path}")

    sub_choice = _fzf(WP_SUBPATHS)
    if sub_choice is None:
        return None

    if sub_choice == "public_html":
        suffix = ""
    elif sub_choice == "custom":
        suffix = input("Enter path after public_html (e.g. wp-content/themes/my-theme): ").strip()
        suffix = suffix.lstrip("/")
    elif sub_choice in ("wp-content/themes", "wp-content/plugins"):
        subdir_name = input(f"Enter name inside {sub_choice}/ : ").strip()
        suffix = f"{sub_choice}/{subdir_name}" if subdir_name else sub_choice
    else:
        suffix = sub_choice

    if "public_html" in base_path:
        parts = base_path.split("public_html")
        root = parts[0] + "public_html"
        remote_path = root if not suffix else root + "/" + suffix.lstrip("/")
    else:
        remote_path = base_path.rstrip("/") + ("/" + suffix.lstrip("/") if suffix else "")

    return remote_path


def _select_local_source(kind: str):
    cwd = os.getcwd()
    console.print(f"\n[cyan]Current directory:[/cyan] {cwd}")

    use_fzf = input("Browse with FZF? (y/n, default y): ").strip().lower()
    if use_fzf in ("", "y"):
        if kind == "folder":
            dirs = [f". (current: {os.path.basename(cwd)})"] + sorted([e.name for e in os.scandir(cwd) if e.is_dir()])
            selected = _fzf(dirs)
            if selected is None:
                return None
            if selected.startswith(". (current"):
                return cwd
            return os.path.join(cwd, selected)
        else:
            items = sorted(f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f)))
            if not items:
                print("[red]No files found in current directory")
                return None
            selected = _fzf(items)
            if selected is None:
                return None
            return os.path.join(cwd, selected)
    else:
        path = input("Enter full local path: ").strip()
        return path


def pushFiles():
    print("[bold blue]Push files to server via rsync[/bold blue]")

    kind = _fzf(["folder", "file"])
    if kind is None:
        return

    local_path = _select_local_source(kind)
    if local_path is None:
        return
    if not os.path.exists(local_path):
        print(f"[red]Local path does not exist: {local_path}")
        return

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
    if not remote_path.endswith("/"):
        remote_path += "/"

    print(
        "\n[yellow]--delete:[/yellow] sync deletes remote files that were removed locally\n"
        "Without --delete: remote keeps files even if deleted locally"
    )
    use_delete = input("Use --delete? (y/n, default n): ").strip().lower()
    delete_flag = ["--delete"] if use_delete == "y" else []

    if kind == "folder":
        sync_choice = input(
            f"Sync folder '{os.path.basename(local_path)}' itself or its contents?\n"
            "  1) folder itself (creates subfolder on server)\n"
            "  2) contents only (merges into remote path)\n"
            "Choice (1/2, default 1): "
        ).strip()
        source = local_path.rstrip("/") + ("/" if sync_choice == "2" else "")
    else:
        source = local_path

    console.print(f"\n[green]Local:[/green]  {source}")
    console.print(f"[green]Remote:[/green] {USERNAME}@{HOST}:{remote_path}")

    confirm = input("\nProceed? (y/n): ").strip().lower()
    if confirm != "y":
        print("[yellow]Cancelled")
        return

    command = [
        "sshpass", "-p", PASSWORD,
        "rsync", "-av", "--progress",
        f"--rsh=sshpass -p {PASSWORD} ssh -p {PORT}",
        *delete_flag,
        source,
        f"{USERNAME}@{HOST}:{remote_path}",
    ]

    print(f"\n[dim]{' '.join(str(c) for c in command)}[/dim]\n")
    subprocess.run(command, check=True)
    notify_send(f"Pushed {source} → {HOST}:{remote_path}")
    print(f"[green]Done: {source} → {HOST}:{remote_path}")
