import os


def getEnv(key: str) -> str:
    return os.environ.get(key)

def getUser():
    return os.getlogin()
