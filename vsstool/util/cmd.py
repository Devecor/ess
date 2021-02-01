import os


def mkdir(dir: str):
    if dir is None:
        return
    if dir is '':
        return
    if os.path.exists(dir):
        return

    print(dir)
    os.mkdir(dir)
