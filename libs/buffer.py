from py_libs.Clipboard import Clipboard
from py_libs.Command import Command


def addToClipBoard(text):
    Clipboard.write(text.strip())


def addToClipBoardFile(file):
    try:
        Command.run_quiet(f"cat {file} | xclip -selection clipboard")
    except RuntimeError:
        pass


def getFromClipBoard():
    return Clipboard.read()
