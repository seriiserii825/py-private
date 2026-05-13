import os
import sys

from rich import print


def checkCsvFiles():
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    required = ["list.csv", "servers.csv"]
    missing = [f for f in required if not os.path.isfile(os.path.join(ROOT_DIR, f))]
    if missing:
        for f in missing:
            print(f"[red]Missing required file: {f}")
        sys.exit(1)
