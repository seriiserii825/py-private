import csv
import os
def getProjectsFromCsv():
    projects = ()
    ROOT_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
    # print(ROOT_DIR)
    csv_file_path = os.path.join(ROOT_DIR, 'list.csv')
    with open(csv_file_path) as my_file:
        reader = csv.reader(my_file, delimiter =',')
        for row in reader:
            project = {
                    'title': row[0],
                    'vps': row[1],
                    'path': row[2],
                    }
            projects = projects + (project,)
    return projects
