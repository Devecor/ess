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


def checkout_item():
    pass


def list_item():
    getdir_cmd = "ss dir"
    res = execute_cmd_with_subprocess(getdir_cmd)
    count = 0
    for i in res.stdout[:-2]:
        if not i.startswith(b"$"):
            count += 1
            print("{:<3d} {}".format(count, bytes2str(i)))
