import sys
import argparse

from vsstool import exec

import logging
logging.basicConfig(level=logging.DEBUG)


def parse_cmd(argv: str):
    argparser = argparse.ArgumentParser(
        description="welcome to elegant vss command line")
    argparser.add_argument("-v", "--version", action="store_const",
                           const=True, default=False, help="查看当前版本")
    argparser.add_argument("-s", "--sync-dir", action="store_const", const=True,
                           default=False, help="让vss当前目录与本地目录保持一致")
    argparser.add_argument("-get", "--get-files", action="store_const", const=True,
                           default=False, help="从vss上取得最新文件（仅当前目录）")

    if len(argv) <= 1:
        return argparser.parse_args(["-h"])
    return argparser.parse_args(argv[1:])


def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = parse_cmd(argv)
    if args.sync_dir:
        exec.sync_dir()
    elif args.version:
        exec.print_version()
    elif args.get_files:
        exec.get_files()


if __name__ == "__main__":
    main(sys.argv)
