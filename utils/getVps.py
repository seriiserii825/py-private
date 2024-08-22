import sys
import os
def getVps():
    ROOT_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
    server_file_path = os.path.join(ROOT_DIR, "servers.csv")
    if not os.path.exists(server_file_path):
        exit("No servers.csv file found")
    with open(server_file_path, "r") as file:
        servers = []
        for line in file:
            name, user, ip, password = line.strip().split(",")
            servers.append({
                "name": name,
                "user": user,
                "ip": ip,
                "password": password
                })
    return servers
