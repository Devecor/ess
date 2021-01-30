import sys
import argparse

from vsstool import exec

import logging

from vsstool.util.config import varify_cwd

logging.basicConfig(level=logging.DEBUG)


def parse_cmd(argv: str):
    argparser = argparse.ArgumentParser(
        description="welcome to elegant vss command line")
    argparser.add_argument("-v", "--version", action="store_const",
                           const=True, default=False, help="查看当前版本")
    argparser.add_argument("-s", "--sync-dir", action="store_const",
                           const=True, default=False,
                           help="同步cwd和所有文件（不含子目录）")
    argparser.add_argument("-l", "--list", action="store_const",
                           const=True, default=False,
                           help="列出当前目录下的所有文件")

    subparsers = argparser.add_subparsers(dest="sub_cmd", help="elegant sub cmd")

    parser_get = subparsers.add_parser("get",
                                       help="从vss上取得最新文件和目录（仅当前目录）")
    parser_get.set_defaults(exec=get_executor)
    parser_get.add_argument("-r", action="store_const",
                            const=True, default=False,
                            help="递归执行")
    parser_get.add_argument("-d", action="store_const",
                            const=True, default=False,
                            help="递归取得所有子目录")

    parser_get = subparsers.add_parser("cho", help="checkout")
    parser_get.set_defaults(exec=checkout_executor)
    parser_get.add_argument("id", nargs="*", default="0", type=int,
                            help="通过序号checkout文件,可指定多个序号")

    if len(argv) <= 1:
        return argparser.parse_args(["-h"])
    return argparser.parse_args(argv[1:])


def get_executor(args):
    if args.d:
        exec.get_dirs(args.r)
        return
    exec.get_item(args.r)


def checkout_executor(args):
    exec.checkout_item()


def main(argv=None):
    args = parse_cmd(sys.argv if argv is None else argv)
    logging.debug(args)
    varify_cwd()

    if args.sync_dir:
        exec.sync_dir()
    elif args.version:
        exec.print_version()
    elif args.list:
        exec.list_item()
    elif args.sub_cmd is not None:
        args.exec(args)


if __name__ == "__main__":
    main(sys.argv)
