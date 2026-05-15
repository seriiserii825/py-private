import os
import shutil
import subprocess
import sys

from rich import print


def _is_arch_linux():
    try:
        with open("/etc/os-release") as f:
            return "arch" in f.read().lower()
    except OSError:
        return False


def checkCsvFiles():
    if not shutil.which("sshpass"):
        if _is_arch_linux() and shutil.which("pacman"):
            print("[yellow]sshpass not found — installing via pacman...")
            result = subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "sshpass"])
            if result.returncode != 0 or not shutil.which("sshpass"):
                print("[red]Failed to install sshpass. Install it manually: sudo pacman -S sshpass")
                sys.exit(1)
            print("[green]sshpass installed successfully.")
        else:
            print("[red]sshpass is not installed. Install it with: sudo pacman -S sshpass")
            sys.exit(1)

    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    required = ["list.csv", "servers.csv"]
    missing = [f for f in required if not os.path.isfile(os.path.join(ROOT_DIR, f))]
    if missing:
        for f in missing:
            print(f"[red]Missing required file: {f}")
        sys.exit(1)
