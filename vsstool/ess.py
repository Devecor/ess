#!/usr/bin/python3

import sys
import argparse

from vsstool import exec

import logging

from vsstool.util.common import str2int
from vsstool.util.config import varify_cwd

ESS_VERSION = "0.0.7-beta"


def parse_cmd(argv: str) -> argparse.Namespace:
    argparser = argparse.ArgumentParser(
        description="here is an elegant command tool for vss by cai.zfeng. enjoy!")
    argparser.add_argument("-v", "--version", action="store_const",
                           const=True, default=False, help="查看当前版本")
    argparser.add_argument("-s", "--sync", action="store_const",
                           const=True, default=False,
                           help="同步所有文件（不含子目录）")
    argparser.add_argument("-l", "--list", action="store_const",
                           const=True, default=False,
                           help="列出当前目录下的所有文件")
    argparser.add_argument("--debug", action="store_const",
                           const=True, default=False,
                           help="debug模式")

    subparsers = argparser.add_subparsers(dest="sub_cmd", help="elegant sub cmd")

    parser_get = subparsers.add_parser("get",
                                       help="从vss上取得最新文件（仅当前目录）")
    parser_get.set_defaults(exec=get_executor)
    parser_get.add_argument("-r", action="store_const",
                            const=True, default=False,
                            help="递归执行")
    parser_get.add_argument("-d", action="store_const",
                            const=True, default=False,
                            help="从vss上取得子目录（仅当前目录）")

    parser_cho = subparsers.add_parser("cho", help="checkout")
    parser_cho.set_defaults(exec=checkout_executor)
    parser_cho.add_argument("id", nargs="*", default="0", type=int,
                            help="通过序号checkout文件,可指定多个序号")
    parser_cho.add_argument("-a", "--all", action="store_const",
                            const=True, default=False,
                            help="checkout所有文件(仅当前目录)")

    parser_chi = subparsers.add_parser("chi", help="checkin")
    parser_chi.set_defaults(exec=checkin_executor)
    parser_chi.add_argument("id", nargs="*", default="0", type=int,
                            help="通过序号checkin文件,可指定多个序号")
    parser_chi.add_argument("-a", "--all", action="store_const",
                            const=True, default=False,
                            help="checkin所有文件(仅当前目录)")

    parser_ucho = subparsers.add_parser("ucho", help="undocheckout")
    parser_ucho.set_defaults(exec=checkin_executor)
    parser_ucho.add_argument("id", nargs="*", default="0", type=int,
                             help="通过序号undocheckout文件,可指定多个序号")
    parser_ucho.add_argument("-a", "--all", action="store_const",
                             const=True, default=False,
                             help="undocheckout所有文件(仅当前目录)")

    if len(argv) <= 1:
        return argparser.parse_args(["-h"])
    return argparser.parse_args(argv[1:])


def get_executor(args):
    if args.d:
        exec.get_dirs(args.r)
        return
    exec.get_files(args.r)


def checkout_executor(args):
    check_series_dispatch(args, exec.CheckSeries.CHECK_OUT)


def checkin_executor(args):
    check_series_dispatch(args, exec.CheckSeries.CHECK_IN)


def undocheckout_executor(args):
    check_series_dispatch(args, exec.CheckSeries.UNDO_CHECK_OUT)


def check_series_dispatch(args: argparse.Namespace, cmdn: exec.CheckSeries):
    if args.all:
        exec.check_series(cmdn, -1)
        return
    if isinstance(args.id, list):
        args.id = str2int(args.id)
        exec.check_series(cmdn, *args.id)
    else:
        exec.check_series(cmdn, int(args.id))


def main(argv=None):
    args = parse_cmd(sys.argv if argv is None else argv)

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    logging.debug(args)
    if args.version:
        exec.print_version(ESS_VERSION)
        return

    varify_cwd()
    exec.sync_dir()

    if args.sync:
        exec.get_files()
    elif args.list:
        exec.list_files()
    elif args.sub_cmd is not None:
        args.exec(args)


if __name__ == "__main__":
    main(sys.argv)
