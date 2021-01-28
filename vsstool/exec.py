import os
import logging
from vsstool.util import config
from vsstool.util.common import getEnv, getUser

def sync():
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
    # os.system()
