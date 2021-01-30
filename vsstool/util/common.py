import logging
import os
import subprocess


def getEnv(key: str) -> str:
    return os.environ.get(key)

def getUser():
    return os.getlogin()

def execute_cmd(cmd: str):
    logging.info(cmd)
    os.system(cmd)

def execute_cmd_with_subprocess(cmd: str):
    res = subprocess.run(cmd.split(), capture_output=True)
    res.stdout = res.stdout.splitlines()
    res.stderr = res.stderr.splitlines()
    logging.info(res)
    return res

def bytes2str(bcode: bytes) -> str:
    try:
        return bcode.decode("utf-8")
    except UnicodeDecodeError:
        pass
    try:
        return bcode.decode("shift_jis")
    except UnicodeDecodeError:
        pass
    return bcode.decode("gbk")
