from pyfzf.pyfzf import FzfPrompt

from modules.Projects import Projects


def copyServerDataToClipboard():
    fzf = FzfPrompt()
    projects_cls = Projects()
    servers = projects_cls.getServersFromCsv()
    selected_server = fzf.prompt(servers)[0]
    print(f"selected_server: {selected_server}")
    server = projects_cls.getServerByName(selected_server)
    print(f"server: {server}")
    projects_cls.copyServerToClipboard(server)
    # projects = projects_cls.getProjects()
    # print(f"projects: {projects}")
    # servers = projects.getServerFromCsv()
    # print(f"servers: {servers}")
