import os
import logging
from vsstool.util import config
from vsstool.util.common import getEnv, getUser


def sync_dir():
    config.UsersConfig().initialize(getEnv('SSDIR'), getUser())
    user_root = config.UsersConfig().root
    info = {
        'cwd': os.getcwd(),
        'login': os.getlogin(),
        'cwdb': os.getcwdb(),
        'pc': os.environ.get("COMPUTERNAME"),
        'user_conf': user_root
    }

    logging.debug(info)
    logging.debug(os.getcwd()[0:len(user_root)])

    if user_root != os.getcwd()[0:len(user_root)]:
        print('当前目录不在{vss_path}中, 请先进入{vss_path}'.format(vss_path=user_root))
        return None
    os.system('ss cp "$/{}"'.format(os.getcwd()[len(user_root):]))


def print_version():
    print('ess 0.0.1')


def get_files(is_recursion=False):
    config.UsersConfig().initialize(getEnv('SSDIR'), getUser())
    user_root = config.UsersConfig().root
    os.system('ss get "$/{dir}\\*"{is_recursion}'.format(dir=os.getcwd()[len(user_root):],
                                                         is_recursion=' -r' if is_recursion else ''))
