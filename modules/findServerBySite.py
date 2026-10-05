import re
import subprocess
from urllib.parse import urlparse

from rich import print
from rich.panel import Panel

from py_libs.Clipboard import Clipboard
from py_libs.Print import Print
from utils.getProjectsFromCsv import getProjectsFromCsv
from utils.getVps import getVps


# example.com, sub.example.co.uk — labels of letters/digits/hyphens,
# alphabetic TLD
DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$"
)


def parseHost(text):
    """Return the domain from a site name or URL, or None if it isn't one."""
    text = text.strip()
    if not text or any(c.isspace() for c in text):
        return None
    # Accept full URLs too: https://example.com/path -> example.com
    try:
        host = urlparse(text if "://" in text else f"//{text}").hostname
    except ValueError:
        return None
    if not host or not DOMAIN_RE.match(host):
        return None
    return host


def findServerBySite():
    site = Clipboard.read()
    host = parseHost(site)
    if not host:
        Print.error(f"Clipboard is not a site name: {site[:100]!r}")
        site = input("Site name (e.g. example.com): ")
        host = parseHost(site)
        if not host:
            Print.error(f"Invalid site name: {site}")
            return
    Print.info(f"Site: {host}")

    # -sn: no port scan, -Pn: don't drop the report if ping is blocked
    result = subprocess.run(
        ["nmap", "-sn", "-Pn", host], capture_output=True, text=True
    )
    match = re.search(r"Nmap scan report for \S+ \(([\d.]+)\)", result.stdout)
    if not match:
        # Valid syntax but no DNS record — not a real site
        Print.error(f"{host} does not resolve to an IP — not a real site?")
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
