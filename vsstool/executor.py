import logging
from typing import List, Callable
from enum import Flag, auto
from vsstool.util.cmd import mkdir, cd, getcwd
from vsstool.util.common import execute_cmd, is_exist, get_cwd_files
from vsstool.util.common import execute_cmd_with_subprocess
from vsstool.util.common import bytes2str
from vsstool.util.config import getAbsoluteDir
import re


class FileOperation(Flag):
    CHECK_OUT = auto()
    CHECK_IN = auto()
    UNDO_CHECK_OUT = auto()
    ADD = auto()


class ListType(Flag):
    LIST_ALL = auto()
    LIST_CHECKED_OUT = auto()


class DirProperty(object):
    PROJECT, CONTENT, LATEST, COMMENT = range(4)


class DirLatest(object):
    VERSION, DATE = range(2)


class FileProperty(object):
    FILE, TYPE, SIZE, MODE, LATEST = range(5)


class FileLatest(object):
    VERSION, DATE = range(2)


class FilePathContext(object):

    def __init__(self, files_provider: Callable):
        self.__files = files_provider()

    @property
    def files(self):
        return self.__files

    def list_files(self):
        show_id_view(self.__files)
        return self.__files


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
    res = execute_cmd_with_subprocess("ss dir -f-")
    cwd = getcwd()
    for i in res.stdout:
        if i.startswith(b"$") and not i.startswith(b"$/"):
            dir = bytes2str(i[1:])
            mkdir(dir)
            if is_recursion:
                cd(dir)
                sync_dir()
                get_dirs(is_recursion=True)
                cd(cwd)


def dispatch_files_operation(operation: FileOperation, *files_id):
    if operation == FileOperation.CHECK_OUT:
        operate_files("checkout", FilePathContext(list_files), *files_id)
    elif operation == FileOperation.CHECK_IN:
        operate_files("checkin", FilePathContext(list_files), *files_id)
    elif operation == FileOperation.UNDO_CHECK_OUT:
        operate_files("undocheckout", FilePathContext(list_files), *files_id)
    elif operation == FileOperation.ADD:
        operate_files("add", FilePathContext(get_staged_files), *files_id)


def check(*args):
    pass

def operate_files(operation: str, context: FilePathContext, *files_id: int):

    """operate files

        使用id来操作文件

        Args:
            operation: "checkout", "checkin", or "undocheckout"
            files_id:
                0:列出可操作id,读取用户输入, 操作相应文件
                -1:操作所有文件
                other_id:操作对应文件
            context: FilePathContext对象
    """

    if len(files_id) == 1:
        if files_id[0] == 0:
            id_inputted = input_id(operation, context.list_files)
            operate_files(operation, context, *id_inputted)
            return
        elif files_id[0] == -1:
            operate_files(operation, context,
                          *[i + 1 for i in range(len(context.files))])
            return
    for i in files_id:
        operate_single_file(operation, context.files[i - 1])


def input_id(action: str, func: Callable) -> List[int]:

    """提示用户输入id

    控制台输出提示信息和备选项, 等待用户输入id(可多选, space隔值)

    Args:
        action: 用于提示用户的操作名, Example: "add"
        func: 用于输入选项信息的回调

    Returns:
        A tuple contains IDs and return value of func
    """

    print("\n 请键入以下id完成{}:".format(action))
    id_max = len(func())
    inputted = input(" 请输入: ").split()
    id_list = []
    for i in inputted:
        if 1 <= int(i) <= id_max:
            id_list.append(int(i))
        else:
            logging.warning(" id应该是{min}-{max},但是你输入了{id},将被忽略".format(
                min="1", max=id_max, id=i))
    return id_list


def operate_single_file(operator, filename: str):
    execute_cmd(f"ss {operator} \"{filename}\" -c-")


def list_files(path="$/"):
    vss_res = execute_cmd_with_subprocess(f"ss dir {path}")
    vss_files = file_filter(vss_res.stdout[:-2])
    return vss_files


def list_dirs(path="$/"):
    vss_res = execute_cmd_with_subprocess(f"ss dir {path} -f-")
    vss_dirs = []
    for i in vss_res.stdout[1:-2]:
        vss_dirs.append(bytes2str(i[1:]))
    return vss_dirs


def list():
    dirs = list_dirs()
    files = list_files()
    dirs.extend(files)
    return dirs


def show_id_view(items: List[int]):
    if items is not None and len(items) > 0:
        print("---------------------------------------------------")
        print(" id  filename")
        print("---------------------------------------------------")
        for i, e in enumerate(items):
            print(" {:<3d} {}".format(i + 1, e))
        print(" ---------------------------------------------------")


def file_filter(files: List[bytes]):

    vss_files = []
    filename_buffer = ''
    files_ = {}
    for i in files:
        files_[i] = bytes2str(i)
    for i in files:
        if not i.startswith(b"$"):
            f = bytes2str(i)
            if len(i) == 78 and f.find('.') == -1:
                filename_buffer += f
                continue

            if len(i) == 68 and f.find('.') == -1:
                filename_buffer += (f + " ")
                continue

            if len(i) < 79:
                if filename_buffer == '':
                    vss_files.append(f)
                else:
                    filename_buffer += f
                    vss_files.append(filename_buffer)
                    filename_buffer = ''
                continue

            if len(i) == 79:
                if is_exist(f):
                    vss_files.append(f)
                else:
                    filename_buffer += f

            if f == filename_buffer:
                continue

            if filename_buffer.find('.') >= 0:
                vss_files.append(filename_buffer)
                filename_buffer = ''
    return vss_files


def get_staged_files():
    vss_files = list_files()
    local_files = get_cwd_files()
    logging.debug({"vss_files": vss_files})
    logging.debug({"local_files": local_files})
    staged_files = []
    for f in local_files:
        if f not in vss_files:
            staged_files.append(f)
    return staged_files


def get_file_properties(filepath: str):
    vss_res = execute_cmd_with_subprocess(f"ss properties \"{filepath}\"")
    vss_prot = parse_file_properties(vss_res.stdout[1:])
    keys = [i for i in vss_prot.keys()]
    latest = vss_prot.get(keys[FileProperty.LATEST])
    latest_keys = [i for i in latest.keys()]
    return [
        vss_prot.get(keys[FileProperty.FILE]),
        latest.get(latest_keys[FileLatest.DATE]),
        "file",
        latest.get(latest_keys[FileLatest.VERSION]),
        vss_prot.get(keys[FileProperty.SIZE]),
    ]


def get_dir_properties(dirpath: str):
    vss_res = execute_cmd_with_subprocess(f"ss properties {dirpath}")
    vss_prot = parse_dir_properties(vss_res.stdout[1:])
    keys = [i for i in vss_prot.keys()]
    latest = vss_prot.get(keys[DirProperty.LATEST])
    latest_keys = [i for i in latest.keys()]
    return [
        vss_prot.get(keys[DirProperty.PROJECT]),
        latest.get(latest_keys[DirLatest.DATE]),
        "project",
        latest.get(latest_keys[DirLatest.VERSION]),
        vss_prot.get(keys[DirProperty.CONTENT])
    ]


def parse_file_status(path="$/"):
    vss_res = execute_cmd_with_subprocess(f"ss status {path}")
    pass


def parse_file_properties(info: List[str]) -> dict:
    rtval = {}
    delimiter = re.compile(": +")
    for i, e in enumerate(info):
        info_line = bytes2str(e)
        match = delimiter.search(info_line)
        if not match:
            rtval_keys = [i for i in rtval.keys()]
            if rtval.get(rtval_keys[-1]) == {}:
                rtval[rtval_keys[-1]] = info_line
            continue
        if not info_line.startswith(" "):
            s = match.span()
            if match.span()[1] == len(info_line):
                rtval[info_line[:match.span()[0]]] = {}
            else:
                rtval[info_line[:match.span()[0]]] = info_line[match.span()[1]:]
        else:
            sub_dict = rtval.get([i for i in rtval.keys()][-1])
            sub_dict[info_line[:match.span()[0]].strip()] = info_line[match.span()[1]:].strip()
    return rtval

def parse_dir_properties(info: List[str]) -> dict:
    rtval = {}
    delimiter = re.compile(": *")
    for i, e in enumerate(info):
        info_line = bytes2str(e)
        match = delimiter.search(info_line)
        if not match:
            last = [i for i in rtval.keys()]
            if rtval[last[-1]] == {}:
                rtval[last[-1]] = bytes2str(e).strip()
            elif isinstance(rtval[last[-1]], str):
                rtval[last[-1]] += bytes2str(e)
            continue
        if not info_line.startswith(" "):
            l = len(info_line)
            if match.span()[1] == len(info_line):
                rtval[info_line[:match.span()[0]]] = {}
            else:
                rtval[info_line[:match.span()[0]]] = info_line[match.span()[1]:]
        else:
            sub_dict = rtval.get([i for i in rtval.keys()][-1])
            sub_dict[info_line[:match.span()[0]].strip()] = info_line[match.span()[1]:].strip()
    return rtval
