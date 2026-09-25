from py_libs.Menu import Menu

from utils.getProjectsFromCsv import getProjectsFromCsv


def viewProjects():
    projects = getProjectsFromCsv()
    rows = [
        [f"[magenta]{p['title']}", f"[green]{p['vps']}", f"[blue]{p['path']}"]
        for p in projects
    ]
    Menu.display("Projects", ["Title", "VPS", "Path"], rows)
