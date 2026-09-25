import os
import subprocess
import time

from rich import print
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from py_libs.Print import Print
from py_libs.Rsync import Rsync

from py_libs.Clipboard import Clipboard
from modules.notifySend import notify_send
from modules.Projects import Projects


def uploadFiles():
    project = Projects()
    project.isCurrentProject()
    HOST = project.project["server_host"]
    PORT = project.project["server_port"] if project.project["server_port"] else 22
    print(f"PORT: {PORT}")
    USERNAME = project.project["server_login"]
    PASSWORD = project.project["server_password"]
    REMOTE_PATH = project.project["server_path"]
    IGNORE_PATTERNS = (
        ".git|.vscode|node_modules|dist|__pycache__|yarn.lock|.idea|vendor"
    )

    REMOTE_PATH = REMOTE_PATH if REMOTE_PATH.endswith("/") else REMOTE_PATH + "/"

    Clipboard.write(PASSWORD)

    def upload_file(file_path):
        print(f"file_path: {file_path}")
        """Upload a file to the remote server."""
        relative_path = os.path.relpath(file_path, ".")
        print(f"PORT upload_file: {PORT}")
        Rsync.push(
            file_path,
            f"{REMOTE_PATH}{relative_path}",
            user=USERNAME,
            host=HOST,
            password=PASSWORD,
            port=PORT,
            flags="-avz --progress",
        )
        notify_send(f"Uploading {file_path} to {REMOTE_PATH}{relative_path}")

    def delete_file(file_path):
        """Delete a file from the remote server."""
        relative_path = os.path.relpath(file_path, ".")
        command = [
            "sshpass",
            "-p",
            PASSWORD,
            "ssh",
            "-p",
            str(PORT),
            "-o",
            "StrictHostKeyChecking=accept-new",
            f"{USERNAME}@{HOST}",
            f"rm -f {REMOTE_PATH}{relative_path}",
        ]
        subprocess.run(command, check=True)
        print(f"Deleting {file_path} from {REMOTE_PATH}{relative_path}")
        notify_send(f"Deleting {file_path} from {REMOTE_PATH}{relative_path}")

    class Watcher(FileSystemEventHandler):
        """Watch for file changes and upload/delete as needed."""

        def on_modified(self, event):
            if not any(
                [pattern in event.src_path for pattern in IGNORE_PATTERNS.split("|")]
            ):
                if event.is_directory:
                    return
                print(f"Detected modification in {event.src_path}")
                upload_file(event.src_path)

        def on_created(self, event):
            if not any(
                [pattern in event.src_path for pattern in IGNORE_PATTERNS.split("|")]
            ):
                if event.is_directory:
                    return
                print(f"Detected creation of {event.src_path}")
                upload_file(event.src_path)

        def on_deleted(self, event):
            if not any(
                [pattern in event.src_path for pattern in IGNORE_PATTERNS.split("|")]
            ):
                if event.is_directory:
                    return
                print(f"Detected deletion of {event.src_path}")
                delete_file(event.src_path)

    def upload_all():
        """Start watching for file changes and upload them."""
        event_handler = Watcher()
        observer = Observer()
        observer.schedule(event_handler, ".", recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def build_upload_dist():
        """Upload the 'dist' folder."""
        subprocess.run(["yarn", "install"], check=True)
        yarn_build = subprocess.run(["yarn", "build"], check=True)
        if yarn_build.returncode != 0:
            Print.error("Failed to build the project.")
            exit(1)
        dist_path = "dist"
        # remove dist on server
        command = [
            "sshpass",
            "-p",
            PASSWORD,
            "ssh",
            "-p",
            str(PORT),
            "-o",
            "StrictHostKeyChecking=accept-new",
            f"{USERNAME}@{HOST}",
            f"rm -rf {REMOTE_PATH}dist",
        ]
        subprocess.run(command, check=True)
        Rsync.push(
            dist_path,
            REMOTE_PATH,
            user=USERNAME,
            host=HOST,
            password=PASSWORD,
            port=PORT,
            flags="-avz --progress",
        )
        # upload front-page on server
        Rsync.push(
            "./functions.php",
            f"{REMOTE_PATH}/functions.php",
            user=USERNAME,
            host=HOST,
            password=PASSWORD,
            port=PORT,
            flags="-avz --progress",
        )
        notify_send(f"Uploading {dist_path} to {REMOTE_PATH}")

    print("1) Upload all files(type 1 or any key, or press enter)")
    print("2) Upload dist folder")

    choice = input("Enter your choice: ")
    if choice.strip() == "2":
        build_upload_dist()
    else:
        upload_all()
