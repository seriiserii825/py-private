import os

import pyperclip as pc


def addToClipBoard(text):
    pc.copy(text.strip())


def addToClipBoardFile(file):
    command = f"cat {file} | xclip -selection clipboard"
    # print(command)
    os.system(command)


def getFromClipBoard():
    text = pc.paste()
    return text
