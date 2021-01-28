import sys
import argparse

from vsstool import exec

import logging
logging.basicConfig(level=logging.DEBUG)


def cmdParse(argv: str):
    argparser = argparse.ArgumentParser(
        description="welcome to elegant vss command line")
    argparser.add_argument("-v", "--version", action="store_const",
                           const=True, default=False, help="查看当前版本")
    argparser.add_argument("-s", "--sync", action="store_const", const=True,
                           default=False, help="让vss当前目录与本地目录保持一致")

    if len(argv) <= 1:
        return argparser.parse_args(["-h"])
    return argparser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = cmdParse(argv)
    if (args.sync):
        exec.sync()


if __name__ == "__main__":
    main(sys.argv)
