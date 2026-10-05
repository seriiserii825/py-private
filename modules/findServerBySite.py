import re
import subprocess
from urllib.parse import urlparse

from rich import print
from rich.panel import Panel

from py_libs.Print import Print
from utils.getProjectsFromCsv import getProjectsFromCsv
from utils.getVps import getVps


def findServerBySite():
    site = input("Site name (e.g. example.com): ").strip()
    if not site:
        Print.error("Empty site name")
        return

    # Accept full URLs too: https://example.com/path -> example.com
    host = urlparse(site if "://" in site else f"//{site}").hostname
    if not host:
        Print.error(f"Invalid site name: {site}")
        return

    # -sn: no port scan, -Pn: don't drop the report if ping is blocked
    result = subprocess.run(
        ["nmap", "-sn", "-Pn", host], capture_output=True, text=True
    )
    match = re.search(r"Nmap scan report for \S+ \(([\d.]+)\)", result.stdout)
    if not match:
        Print.error(f"Could not resolve IP for {host}")
        print(result.stdout or result.stderr)
        return

    ip = match.group(1)
    servers = [vps["name"] for vps in getVps() if vps["ip"] == ip]
    header = f"{host} → [yellow]{ip}[/yellow]"
    if not servers:
        print(Panel(f"{header}\n[red]No server found in servers.csv"))
        return

    # Several accounts can share one IP — narrow down by project paths
    # in list.csv that contain the domain (e.g. /web/<domain>/public_html)
    exact = sorted({
        p["vps"] for p in getProjectsFromCsv()
        if f"/{host}/" in p["path"] and p["vps"] in servers
    })
    lines = [header]
    if exact:
        lines.append(f"Server: [bold green]{', '.join(exact)}")
    lines.append(f"Same IP: [dim]{', '.join(servers)}")
    print(Panel("\n".join(lines)))
