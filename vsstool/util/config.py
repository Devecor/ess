import logging
import re
import threading
import configparser

from vsstool.util.cmd import getcwd
from vsstool.util.common import get_env, get_user

SS_DB_INI = "srcsafe.ini"
SS_USERS_TEXT = "users.txt"


class UsersConfig(object):

    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __initialize(self, ssdir=get_env("SSDIR"), user=get_user()):

        '''读取users.txt文件, 取得用户配置目录'''

        self.__ssdir = ssdir if ssdir[-1] == '\\' else ssdir + '\\'
        self.__user_name = user

        users_text_path = ssdir + '\\' + SS_USERS_TEXT
        logging.info('parsing ' + users_text_path)

        homes = dict()
        with open(users_text_path, 'r') as users_text:
            lines = users_text.readlines()
            for i in lines:
                user_name, user_home = self.__split(i.lower()[0:-1])
                homes[user_name] = user_home
            users_text.close()

        self.__user_home = homes.get(self.__user_name.lower())
        self.__parse_config_file()

        logging.debug({'user_home': self.__user_home})
        logging.debug({'user_root': self.__root})

    def __new__(cls, *args, **kwargs):
        if not hasattr(UsersConfig, "_instance"):
            with UsersConfig._instance_lock:
                if not hasattr(UsersConfig, "_instance"):
                    UsersConfig._instance = object.__new__(cls)
                    UsersConfig._instance.__initialize()
        return UsersConfig._instance

    def __parse_config_file(self):
        config_file = self.__ssdir + self.__user_home
        logging.info('parsing {}'.format(config_file))

        file_content = ''
        with open(config_file) as f:
            file_content = '[top]\n' + f.read()
            f.close()

        user_config = configparser.ConfigParser()
        user_config.read_string(file_content)

        self.__root = user_config.get('$/', self.__get_dir_key())

    @staticmethod
    def __get_dir_key():
        return 'Dir ({})'.format(get_env("COMPUTERNAME"))

    @staticmethod
    def __split(line: str):
        return re.sub('\\s*=\\s*', '=', line, 1).split('=')

    def __str__(self):
        return {'root': self.__root}.__str__()

    @property
    def root(self) -> str:
        if self.__root is None:
            raise RuntimeError('{} is uninitialized, initialize first please.'
                               .format(self.__class__.__name__))
        return self.__root


def verify_cwd():
    user_root = UsersConfig().root
    if user_root != getcwd()[:len(user_root)]:
        print('当前目录不在{vss_path}中, 请先进入{vss_path}'.format(vss_path=user_root))
        import sys
        sys.exit()


def getAbsoluteDir():
    user_root = UsersConfig().root
    cwd = getcwd()[len(user_root) + 1:]
    return "$/" + cwd.replace("\\", "/")


def absolute2relative(abs: str):
    pwd = getAbsoluteDir()
    if pwd == abs[:len(pwd)]:
        return abs[len(pwd) + 1:]
    else:
        logging.info("abs: " + abs)
        logging.debug("pwd: " + pwd)
        raise RuntimeError("inner error")
