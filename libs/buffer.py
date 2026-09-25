import pyperclip as pc

from py_libs.Command import Command


def addToClipBoard(text):
    pc.copy(text.strip())


def addToClipBoardFile(file):
    try:
        Command.run_quiet(f"cat {file} | xclip -selection clipboard")
    except RuntimeError:
        pass


def getFromClipBoard():
    text = pc.paste()
    return text
