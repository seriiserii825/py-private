import subprocess


def notify_send(message):
    """Send a notification using notify-send."""
    subprocess.run(['notify-send', message], check=True)
