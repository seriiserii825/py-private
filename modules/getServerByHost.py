import os

from py_libs.CsvFile import CsvFile

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def getServerByHost(host_name):
    file_path = os.path.join(ROOT_DIR, "servers.csv")
    rows = CsvFile(file_path).read_csv() or []
    for row in rows:
        fields = [row["name"], row["username"], row["ip"], row["password"]]
        if row.get("port"):
            fields.append(row["port"])
        if host_name in ",".join(fields):
            return fields
    return None
