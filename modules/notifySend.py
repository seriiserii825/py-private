from py_libs.Notification import Notification


def notify_send(message):
    """Send a notification using notify-send."""
    Notification("py-private", message).notify()
