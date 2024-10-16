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
            data = line.strip().split(",")
            name = data[0]
            user = data[1]
            ip = data[2]
            password = data[3]
            port = data[4] if len(data) > 4 else 22
            servers.append({
                "name": name,
                "user": user,
                "ip": ip,
                "password": password,
                "port": port
                })
    return servers
