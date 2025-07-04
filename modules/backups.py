import os

from termcolor import colored

from libs.buffer import addToClipBoard
from utils.getProjects import getProjects
from utils.getVps import getVps
from utils.selectWpressFile import selectWpressFiles


def backups():
    if not os.path.exists("style.css"):
        print(colored("File style.css does  not exist", "red"))
        exit(1)
    current_dir_path = os.getcwd()
    theme_name = os.path.basename(current_dir_path)
    projects = getProjects(theme_name)
    wpress_file = selectWpressFiles()

    print(colored(f"File: {wpress_file}", "blue"))
    for project in projects:
        if project["title"] == theme_name:
            vps = project["vps"]
            vps_list = getVps()
            vps_item = next((item for item in vps_list if item["name"] == vps), None)
            print(f"vps_item: {vps_item}")
            if vps_item is None:
                print(colored(f"VPS {vps} not found", "red"))
                exit(1)
            vps_pass = vps_item["password"]
            vps_port = vps_item["port"]
            vps_path = project["path"]
            # if not exists str wp-content/ai1wm-backups in vps_path
            if not "wp-content" in vps_path:
                print(colored(f"Path {vps_path} is not correct", "red"))
                exit(1)
            path_arr = vps_path.split("/")
            path_to_aimwp = "/".join(path_arr[:-2]) + "/ai1wm-backups"
            vps_url = f"{vps_item['user']}@{vps_item['ip']}"
            # vps_command = f"rsync -avP '{wpress_file}' {vps_url}:{vps_path}"
            addToClipBoard(vps_pass)
            vps_command = f"rsync -avP -e 'ssh -p {vps_port}' \
                    '{wpress_file}' {vps_url}:{path_to_aimwp}"
            print(colored(f"VPS command: {vps_command}", "blue"))
            os.system(vps_command)
            print(colored("File copied", "green"))
            break
