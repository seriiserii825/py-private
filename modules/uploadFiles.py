import os
import subprocess
import time

from rich import print
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from libs.buffer import addToClipBoard
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

    addToClipBoard(PASSWORD)

    def notify_send(message):
        """Send a notification using notify-send."""
        subprocess.run(["notify-send", message], check=True)

    def upload_file(file_path):
        print(f"file_path: {file_path}")
        """Upload a file to the remote server."""
        relative_path = os.path.relpath(file_path, ".")
        print(f"PORT upload_file: {PORT}")
        command = [
            "sshpass",
            "-p",
            PASSWORD,
            "rsync",
            "-avz",
            "--progress",
            f"--rsh=sshpass -p {PASSWORD} ssh -p {PORT}",
            file_path,
            f"{USERNAME}@{HOST}:{REMOTE_PATH}{relative_path}",
        ]
        # command = [
        #     "sshpass", "-p", PASSWORD, "rsync", "-avz", "--progress",
        #     "-e", f"ssh -p {PORT}",
        #     file_path, f"{USERNAME}@{HOST}:{REMOTE_PATH}{relative_path}"
        # ]
        print(command)
        subprocess.run(command, check=True)
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
            print("[red]Failed to build the project.")
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
            f"{USERNAME}@{HOST}",
            f"rm -rf {REMOTE_PATH}dist",
        ]
        subprocess.run(command, check=True)
        command = [
            "sshpass",
            "-p",
            PASSWORD,
            "rsync",
            "-avz",
            "--progress",
            f"--rsh=sshpass -p {PASSWORD} ssh -p {PORT}",
            dist_path,
            f"{USERNAME}@{HOST}:{REMOTE_PATH}",
        ]
        print(f"command: {command}")
        subprocess.run(command, check=True)
        # upload front-page on server
        command = [
            "sshpass",
            "-p",
            PASSWORD,
            "rsync",
            "-avz",
            "--progress",
            f"--rsh=sshpass -p {PASSWORD} ssh -p {PORT}",
            "./functions.php",
            f"{USERNAME}@{HOST}:{REMOTE_PATH}/functions.php",
        ]
        subprocess.run(command, check=True)
        print(f"command: {command}")
        notify_send(f"Uploading {dist_path} to {REMOTE_PATH}")

    print("1) Upload all files(type 1 or any key, or press enter)")
    print("2) Upload dist folder")

    choice = input("Enter your choice: ")
    if choice.strip() == "2":
        build_upload_dist()
    else:
        upload_all()
