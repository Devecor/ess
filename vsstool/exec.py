import logging
from typing import List, Callable
from enum import Flag, auto
from vsstool.util.cmd import mkdir, cd, getcwd
from vsstool.util.common import execute_cmd, is_exist, get_cwd_files
from vsstool.util.common import execute_cmd_with_subprocess
from vsstool.util.common import bytes2str
from vsstool.util.config import getAbsoluteDir


class FileOperation(Flag):
    CHECK_OUT = auto()
    CHECK_IN = auto()
    UNDO_CHECK_OUT = auto()
    ADD = auto()


class ListType(Flag):
    LIST_ALL = auto()
    LIST_CHECKED_OUT = auto()


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


def list_files():
    vss_res = execute_cmd_with_subprocess("ss dir")
    vss_files = file_filter(vss_res.stdout[:-2])
    return vss_files


def show_id_view(items: List[int]):
    if items is not None and len(items) > 0:
        print("---------------------------------------------------")
        print(" id  filename")
        print("---------------------------------------------------")
        for i, e in enumerate(items):
            print(" {:<3d} {}".format(i + 1, e))
        print(" ---------------------------------------------------")


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
