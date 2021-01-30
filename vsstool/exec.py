import logging
from typing import List

from vsstool.util.cmd import mkdir
from vsstool.util.common import execute_cmd, execute_cmd_with_subprocess
from vsstool.util.common import bytes2str
from vsstool.util.config import getAbsoluteDir


def sync_dir():
    cmd = 'ss cp "{dir}"'.format(dir=getAbsoluteDir())
    execute_cmd(cmd)
    get_item()


def print_version():
    print('ess 0.0.1')


def get_item(is_recursion=False):
    cmd = 'ss get "{dir}\\*"{is_recursion}'\
        .format(dir=getAbsoluteDir(),
                is_recursion=' -r' if is_recursion else '')
    execute_cmd(cmd)


def get_dirs(is_recursion=False):
    getdir_cmd = "ss dir{}".format(' -r' if is_recursion else '')
    res = execute_cmd_with_subprocess(getdir_cmd)
    for i in res.stdout:
        if is_recursion:
            if i.startswith(b"$/") and i.endswith(b":"):
                mkdir(bytes2str(i[2:-1]))
        else:
            if i.startswith(b"$") and not i.endswith(b":"):
                mkdir(bytes2str(i[1:]))


def checkout_file(id: int):
    if id == -1:
        execute_cmd("ss checkout *")
        return
    files = list_files(visibility=False)
    if 0 < id <= len(files):
        execute_cmd("ss checkout {}".format(files[id - 1]))
    else:
        logging.warning("id应该是0-{},但是你输入了{}".format(len(files), id))


def checkout_files(*id: int):
    if len(id) == 1 and id[0] == 0:
        id_inputted = input_id("checkout")
        checkout_files(*id_inputted)
        return
    for i in id:
        checkout_file(i)


def input_id(action: str) -> List[int]:
    print("请键入以下id完成{}:".format(action))
    max = len(list_files())
    inputted = input("请输入:").split()
    rtval = []
    for i in inputted:
        if 1 <= int(i) <= max:
            rtval.append(int(i))
        else:
            logging.warning("id应该是{min}-{max},但是你输入了{id},将被忽略".format(
                min="1", max=max, id=i))
    return rtval

def list_files(visibility=True):
    getdir_cmd = "ss dir"
    res = execute_cmd_with_subprocess(getdir_cmd)
    files = []
    count = 0
    for i in res.stdout[:-2]:
        if not i.startswith(b"$"):
            files.append(bytes2str(i))
            if visibility:
                count += 1
                print("{:<3d} {}".format(count, bytes2str(i)))
    return files
