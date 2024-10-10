import os

ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
def getServerByHost(host_name):
    file_path = os.path.join(ROOT_DIR, "servers.csv")
    with open(file_path, "r") as file:
        for line in file:
            if host_name in line:
                return line.split(",")
    return None
