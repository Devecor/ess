import logging
import os
import subprocess
from datetime import datetime
from typing import List


def get_env(key: str) -> str:
    return os.environ.get(key)


def get_user():
    return os.getlogin()


def execute_cmd(cmd: str):
    logging.info(cmd)
    os.system(cmd)


def execute_cmd_with_subprocess(cmd: str):
    logging.info(cmd)
    res = subprocess.run(cmd, capture_output=True, shell=True)
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


def is_exist(filename: str) -> bool:
    return os.path.exists(filename)


def is_dir(path: str) -> bool:
    return os.path.isdir(path)


def is_file(path: str) -> bool:
    return os.path.isfile(path)


def get_cwd_files():
    current_dirs = os.listdir()
    files = []
    for i in current_dirs:
        if os.path.isfile(i):
            files.append(i)
    return files


def get_tail(path: str):
    return path.split("/")[-1]


def get_base_dir(filepath: str):
    return os.path.dirname(filepath)


def open_file(filepath: str):
    os.startfile(filepath)


def get_file_timestamp(filepath: str):
    m = os.path.getmtime(filepath)
    fm = datetime.fromtimestamp(m).strftime("%Y/%m/%d %#H:%M:%S")
    return fm
