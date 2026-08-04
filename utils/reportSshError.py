from rich import print
from rich.panel import Panel

SSHPASS_EXIT_CODES = {
    1: "Invalid command line argument",
    2: "Conflicting arguments given",
    3: "General runtime error of sshpass",
    4: "Unrecognized response from ssh (parse error)",
    5: "Invalid/incorrect password",
    6: "Host public key is unknown, sshpass exits without confirming it",
}


def reportSshError(returncode: int) -> None:
    if returncode == 0:
        return
    default = (
        f"ssh exited with code {returncode}"
        if returncode == 255
        else f"Unknown error (exit code {returncode})"
    )
    message = SSHPASS_EXIT_CODES.get(returncode, default)
    print(Panel(f"[red]Connection failed: {message}"))
