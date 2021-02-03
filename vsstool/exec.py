import logging
from typing import List, Optional
from enum import Flag, auto
from vsstool.util.cmd import mkdir
from vsstool.util.common import execute_cmd, is_exist
from vsstool.util.common import execute_cmd_with_subprocess
from vsstool.util.common import bytes2str
from vsstool.util.config import getAbsoluteDir
from vsstool.util.config import absolute2relative


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


def print_version(v: str):
    print("ess " + v)


def get_files(is_recursion=False):
    cmd = 'ss get "{dir}\\*"{is_recursion}'\
        .format(dir=getAbsoluteDir(),
                is_recursion=' -r' if is_recursion else '')
    execute_cmd(cmd)


def get_dirs(is_recursion=False):
    cmd = "ss dir{}".format(' -r' if is_recursion else '')
    res = execute_cmd_with_subprocess(cmd)
    for i in res.stdout:
        if is_recursion:
            if i.startswith(b"$/") and i.endswith(b":"):
                path = absolute2relative(bytes2str(i[:-1]))
                mkdir(path)
        else:
            if i.startswith(b"$") and not i.endswith(b":"):
                mkdir(bytes2str(i[1:]))


def check_series(cmdn: CheckSeries, *files_id):
    if cmdn == CheckSeries.CHECK_OUT:
        operate_files("checkout", *files_id)
    elif cmdn == CheckSeries.CHECK_IN:
        operate_files("checkin", *files_id)
    elif cmdn == CheckSeries.UNDO_CHECK_OUT:
        operate_files("undocheckout", *files_id)


def operate_files(operator: str, *files_id: int):
    if len(files_id) == 1 and files_id[0] == 0:
        id_inputted = input_id(operator)
        operate_files(operator, *id_inputted)
        return
    for i in files_id:
        operate_single_file(operator, i)


def input_id(action: str) -> List[int]:
    print("\n 请键入以下id完成{}:".format(action))
    id_max = len(list_files())
    inputted = input(" 请输入:").split()
    rtval = []
    for i in inputted:
        if 1 <= int(i) <= id_max:
            rtval.append(int(i))
        else:
            logging.warning(" id应该是{min}-{max},但是你输入了{id},将被忽略".format(
                min="1", max=id_max, id=i))
    return rtval


def operate_single_file(operator, fileid: int):

    """checkout files

    使用id来操作文件

    Args:
        operator: "checkout", "checkin", or "undocheckout"
        fileid: 0:列出文件id,读取用户输入, 操作相应文件
            -1:操作所有文件
            other_id:操作对应文件
    """

    if fileid == -1:
        execute_cmd(f"ss {operator} * -c-")
        return
    files = list_files(visibility=False)
    if 0 < fileid <= len(files):
        execute_cmd("ss {operator} \"{id}\" -c-".format(operator=operator,
                                                        id=files[fileid - 1]))
    else:
        logging.warning(" id应该是0-{},但是你输入了{}".format(len(files), fileid))


def list_files(visibility=True):
    vss_res = execute_cmd_with_subprocess("ss dir")
    vss_files = file_filter(vss_res.stdout[:-2])
    if visibility and len(vss_files) > 0:
        print(" ---------------------------------------------------")
        print(" id  filename")
        print(" ---------------------------------------------------")
        for i, e in enumerate(vss_files):
            print(" {:<3d} {}".format(i + 1, e))
        print(" ---------------------------------------------------")
    return vss_files


def file_filter(files: List[bytes]):

    """这是一段很难看懂的代码， 下次一定干掉"""

    vss_files = []
    filename_buffer = ''
    for i in files:
        if not i.startswith(b"$"):
            f = bytes2str(i)

            if len(f) < 79:
                if filename_buffer == '':
                    vss_files.append(f)
                    continue
                else:
                    filename_buffer += f
                    vss_files.append(filename_buffer)
                    filename_buffer = ''
                    continue
            if len(f) == 79:
                if is_exist(f):
                    vss_files.append(f)
                    continue
                else:
                    filename_buffer += f
            if filename_buffer.find('.') >= 0:
                vss_files.append(filename_buffer)
                filename_buffer = ''
    return vss_files
