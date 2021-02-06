import logging
import os


def mkdir(dir: str):
    if dir is None:
        return
    if dir is '':
        return
    if os.path.exists(dir):
        return

    print("mkdir " + dir)
    os.mkdir(dir)

def cd(dir: str):
    logging.debug("cd " + dir)
    os.chdir(dir)

def getcwd():
    return os.getcwd()