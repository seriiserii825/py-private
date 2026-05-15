import os
import shutil
import sys

from rich import print


def checkCsvFiles():
    if not shutil.which("sshpass"):
        print("[red]sshpass is not installed. Install it with: sudo pacman -S sshpass")
        sys.exit(1)

    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    required = ["list.csv", "servers.csv"]
    missing = [f for f in required if not os.path.isfile(os.path.join(ROOT_DIR, f))]
    if missing:
        for f in missing:
            print(f"[red]Missing required file: {f}")
        sys.exit(1)
