import os

from py_libs.CsvFile import CsvFile


def getProjectsFromCsv():
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_file_path = os.path.join(ROOT_DIR, "list.csv")
    rows = CsvFile(csv_file_path).read_csv() or []
    return tuple(
        {"title": row["title"], "vps": row["vps"], "path": row["path"]}
        for row in rows
    )
