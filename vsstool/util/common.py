import logging
import os
import subprocess
from typing import List


def getEnv(key: str) -> str:
    return os.environ.get(key)


def getUser():
    return os.getlogin()


def execute_cmd(cmd: str):
    logging.info(cmd)
    os.system(cmd)


def execute_cmd_with_subprocess(cmd: str):
    logging.info(cmd.split())
    res = subprocess.run(cmd.split(), capture_output=True, shell=True)
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


def str2int(strl: List[str]):
    rtval = []
    for i in strl:
        rtval.append(int(i))
    return rtval


def isExist(filename: str) -> bool:
    return os.path.exists(filename)
