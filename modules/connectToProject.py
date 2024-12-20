import os
from libs.buffer import addToClipBoard
from utils.getProjectsFromCsv import getProjectsFromCsv
from pyfzf.pyfzf import FzfPrompt

from utils.getVps import getVps
fzf = FzfPrompt()

def connectToProject():
    projects = getProjectsFromCsv()
    projects_titles = [project['title'] for project in projects]
    selected_project = fzf.prompt(projects_titles)
    vps_list = getVps()
    for project in projects:
        if project['title'] == selected_project[0]:
            for vps in vps_list:
                if vps['name'] == project['vps']:
                    server_password = vps['password']
                    server_port = vps['port']
                    new_path = project['path']
                    addToClipBoard(server_password)
                    command = f"ssh -t -p {server_port} {vps['user']}@{vps['ip']} \"cd {new_path} ; bash --login\" "
                    print(f"Command: {command}")
                    os.system(command)
                    break
            break
