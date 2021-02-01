import os


def mkdir(dir: str):
    if dir is None:
        return
    if os.path.exists(dir):
        return
    os.mkdir(dir)
    print(dir)
