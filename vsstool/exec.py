import logging
from typing import List, Optional
from enum import Flag, auto
from vsstool.util.cmd import mkdir
from vsstool.util.common import execute_cmd, isExist
from vsstool.util.common import execute_cmd_with_subprocess
from vsstool.util.common import bytes2str
from vsstool.util.config import getAbsoluteDir


class CheckSeries(Flag):
    CHECK_OUT = auto()
    CHECK_IN = auto()
    UNDO_CHECK_OUT = auto()


class ListType(Flag):
    LIST_ALL = auto()
    LIST_CHECKED_OUT = auto()


def sync_dir():
    cmd = 'ss cp "{dir}"'.format(dir=getAbsoluteDir())
    execute_cmd(cmd)
    get_files()


def print_version(v: str):
    print("ess " + v)


def get_files(is_recursion=False):
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


def check_series(cmdn: CheckSeries, *id):
    if cmdn == CheckSeries.CHECK_OUT:
        operate_files("checkout", *id)
    elif cmdn == CheckSeries.CHECK_IN:
        operate_files("checkin", *id)
    elif cmdn == CheckSeries.UNDO_CHECK_OUT:
        operate_files("undocheckout", *id)


def operate_files(operator: str, *id: int):
    if len(id) == 1 and id[0] == 0:
        id_inputted = input_id(operator)
        operate_files(operator, *id_inputted)
        return
    for i in id:
        operate_single_file(operator, i)


def input_id(action: str) -> List[int]:
    print("\n 请键入以下id完成{}:".format(action))
    max = len(list_files())
    inputted = input(" 请输入:").split()
    rtval = []
    for i in inputted:
        if 1 <= int(i) <= max:
            rtval.append(int(i))
        else:
            logging.warning(" id应该是{min}-{max},但是你输入了{id},将被忽略".format(
                min="1", max=max, id=i))
    return rtval


def operate_single_file(operator, id: int):

    """checkout files

    使用id来签出文件

    Args:
        operator: "checkout", "checkin", or "undocheckout"
        id: 0:列出文件id,读取用户输入, 签出相应文件
            -1:签出所有文件
            other_id:签出对应文件
    """

    if id == -1:
        execute_cmd(f"ss {operator} * -c-")
        return
    files = list_files(visibility=False)
    if 0 < id <= len(files):
        execute_cmd("ss {operator} {id} -c-".format(operator=operator,
                                                    id=files[id - 1]))
    else:
        logging.warning(" id应该是0-{},但是你输入了{}".format(len(files), id))


def list_files(visibility=True):
    vss_res = execute_cmd_with_subprocess("ss dir")
    vss_files = file_filter(vss_res.stdout[:-2])
    if visibility:
        print(" ---------------------------------------------------")
        print(" id  filename")
        print(" ---------------------------------------------------")
        for i, e in enumerate(vss_files):
            print(" {:<3d} {}".format(i + 1, e))
        print(" ---------------------------------------------------")
    return vss_files


def file_filter(files: List[str]):
    vss_files = []
    for i in files:
        if not i.startswith(b"$"):
            f = bytes2str(i)
            if isExist(f):
                vss_files.append(f)
            else:    # 为了支持长文件名，这里做个妥协
                exact_f = get_exact_filename(i)
                if exact_f is not None:
                    f = exact_f
                    vss_files.append(exact_f)
    return vss_files


def get_exact_filename(partyfile: bytes) -> Optional[str]:
    local_res = execute_cmd_with_subprocess("dir")
    for i in local_res.stdout:
        if i.startswith(partyfile):
            return bytes2str(i)
    return None
