import os


def mkdir(dir: str):
    if dir == "":
        return
    os.mkdir(dir)
    print(dir)