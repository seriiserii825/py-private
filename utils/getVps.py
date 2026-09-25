import os

from py_libs.CsvFile import CsvFile


def getVps():
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    server_file_path = os.path.join(ROOT_DIR, "servers.csv")
    if not os.path.exists(server_file_path):
        exit("No servers.csv file found")
    rows = CsvFile(server_file_path).read_csv() or []
    return [
        {
            "name": row["name"],
            "user": row["username"],
            "ip": row["ip"],
            "password": row["password"],
            "port": row["port"] if row.get("port") else 22,
        }
        for row in rows
    ]
