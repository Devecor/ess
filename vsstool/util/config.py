import logging
import re
import threading
import configparser
import os

SS_DB_INI = "srcsafe.ini"
SS_USERS_TEXT = "users.txt"


class UsersConfig(object):

    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def initialize(self, ssdir: str, user: str):

        '''读取users.txt文件, 取得用户配置目录'''

        self.__ssdir = ssdir if ssdir[-1] == '\\' else ssdir + '\\'
        self.__user_name = user

        users_text_path = ssdir + '\\' + SS_USERS_TEXT
        logging.info('parsing ' + users_text_path)

        homes = dict()
        with open(users_text_path, 'r') as users_text:
            lines = users_text.readlines()
            for i in lines:
                user_name, user_home = self.__split(i[0:-1])
                homes[user_name] = user_home
            users_text.close()

        self.__user_home = homes.get(user)
        self.__parseConfigFile()

        logging.debug({'user_home': self.__user_home})
        logging.debug({'user_root': self.__root})

    def __split(self, line: str):
        return re.sub('\\s*=\\s*', '=', line, 1).split('=')

    def __new__(cls, *args, **kwargs):
        if not hasattr(UsersConfig, "_instance"):
            with UsersConfig._instance_lock:
                if not hasattr(UsersConfig, "_instance"):
                    UsersConfig._instance = object.__new__(cls)
        return UsersConfig._instance

    def __parseConfigFile(self):
        config_file = self.__ssdir + self.__user_home
        logging.info('parsing {}'.format(config_file))

        file_content = ''
        with open(config_file) as f:
            file_content = '[top]\n' + f.read()
            f.close()

        user_config = configparser.ConfigParser()
        user_config.read_string(file_content)

        self.__root = user_config.get('$/', self.__getDirKey())

        logging.info(self.__root)

    def __getDirKey(self):
        return 'Dir ({})'.format(os.environ.get("COMPUTERNAME"))

    def __str__(self):
        return {'root': self.__root}.__str__()

    @property
    def root(self) -> str:
        if self.__root is None:
            raise RuntimeError('{} is uninitialized, initialize first please.'
                               .format(self.__class__.__name__))
        return self.__root