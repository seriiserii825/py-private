import os

from py_libs.Print import Print
from py_libs.Rsync import Rsync

from py_libs.Clipboard import Clipboard
from modules.notifySend import notify_send
from utils.getProjects import getProjects
from utils.getVps import getVps
from utils.selectWpressFile import selectWpressFiles


def backups():
    if not os.path.exists("style.css"):
        Print.error("File style.css does  not exist")
        exit(1)
    current_dir_path = os.getcwd()
    theme_name = os.path.basename(current_dir_path)
    projects = getProjects(theme_name)
    wpress_file = selectWpressFiles()

    Print.info(f"File: {wpress_file}")
    for project in projects:
        if project["title"] == theme_name:
            vps = project["vps"]
            vps_list = getVps()
            vps_item = next(
                (item for item in vps_list if item["name"] == vps), None)
            print(f"vps_item: {vps_item}")
            if vps_item is None:
                Print.error(f"VPS {vps} not found")
                exit(1)
            vps_pass = vps_item["password"]
            vps_port = vps_item["port"]
            vps_path = project["path"]
            # if not exists str wp-content/ai1wm-backups in vps_path
            if not "wp-content" in vps_path:
                Print.error(f"Path {vps_path} is not correct")
                exit(1)
            path_arr = vps_path.split("/")
            path_to_aimwp = "/".join(path_arr[:-2]) + "/ai1wm-backups"
            Clipboard.write(vps_pass)
            Rsync.push(
                wpress_file,
                path_to_aimwp,
                user=vps_item["user"],
                host=vps_item["ip"],
                password=vps_pass,  # ggignore
                port=vps_port,
                flags="-avP",
            )
            Print.success("File copied")
            notify_send(
                f"Copied {os.path.basename(wpress_file)} to {path_to_aimwp}")
            break
