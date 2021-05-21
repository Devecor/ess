import json

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QStandardItemModel, QBrush, QColor

from vsstool.util.cmd import mkdir, cd
from vsstool.util.common import get_base_dir, is_exist, execute_cmd, open_file, \
    execute_cmd_with_subprocess, bytes2str

from essexp.model import ItemSettingContext, EssStandardItem, EssModelIndex
import threading

from vsstool.util.config import getLocals

ITEM_PROPERTIES = ["name", "date", "type", "version", "size", "user"]


def set_icon(item: EssStandardItem, path: str):
    icon = QIcon()
    icon.addFile(path, QSize(), QIcon.Normal, QIcon.On)
    item.setIcon(icon)


def get_item_by_index(index: EssModelIndex, model: QStandardItemModel) -> EssStandardItem:
    ancestor_indexes = [index]
    while index.parent() != EssModelIndex():
        ancestor_indexes.append(index.parent())
        index = index.parent()
    ancestor_indexes.reverse()
    item = model.invisibleRootItem()
    for ancestor in ancestor_indexes:
        item = item.child(ancestor.row(), ancestor.column())
    return item


def row_item_provider(d: dict, name: str):
    """
    目录树节点生成和设定
    :param d: 节点数据: {name:{...}}
    :param name: target name for setting
    :return: EssStandardItem
    """
    row = EssStandardItem(name)
    detail = d.get(name)
    row.ss_type = detail.get("type")
    row.ss_cho = detail.get("ischeckout")
    row.setAccessibleText(detail.get("spec"))

    if detail.get("type") == "project":
        set_icon(row, u":/folder/fold.svg")
    else:
        if detail.get("ischeckout"):
            row.setForeground(QBrush(QColor("red")))
            set_icon(row, u":/checkout/checkoutline02.svg")
        else:
            set_icon(row, u":/file/file.svg")

    return row


def update_item_data(context: ItemSettingContext):
    items = get_from_essharp(context.text(), "n")
    for i, d in enumerate(items.keys()):
        item_i = row_item_provider(items, d)
        context.set(i, 0, item_i)

        # 只取得文件名的情况: 空item设定
        for j, t in enumerate(ITEM_PROPERTIES[1:]):
            item_j = EssStandardItem("")
            item_j.ss_type = t
            context.set(i, j + 1, item_j)

        threading.Thread(target=update_item_props,
                         args=(items[d].get("spec"), i, context)).start()


def update_item_props(path: str, row, context):
    vss_res = get_from_essharp(path, "d")

    if not len(vss_res):
        context.on_error()
        return

    props = [
        vss_res["version_info"]["date"],
        vss_res["type"],
        vss_res["version_number"],
        str(vss_res["size"] // 1024) + "KB" if str(vss_res["size"]).isdigit() else vss_res["size"],
        vss_res["version_info"]["user_name"],
    ]

    for j, d in enumerate(props):
        item_j = EssStandardItem(str(d))
        item_j.ss_type = ITEM_PROPERTIES[j+1]
        context.set(row, j + 1, item_j)


def update_item_data_on_error(context: ItemSettingContext):
    items = get_from_essharp(context.text(), 'l')
    for i, d in enumerate(items.keys()):
        item_i = row_item_provider(items, d)
        context.set(i, 0, item_i)

        props = [
            items[d]["version_info"]["date"],
            items[d]["type"],
            items[d]["version_number"],
            str(items[d]["size"] // 1024) + "KB" if str(items[d]["size"]).isdigit() else items[d]["size"],
            items[d]["version_info"]["user_name"],
        ]

        for j, e in enumerate(props):
            item_j = EssStandardItem(str(e))
            item_j.ss_type = ITEM_PROPERTIES[j + 1]
            context.set(i, j + 1, item_j)


def open_file_by_ss(fullname: str, override=False) -> bool:
    if override:
        get_file(fullname)
    path = getLocals(fullname)
    if is_exist(path):
        open_file(path)
        return True
    return False


def get_from_essharp(path, opt) -> dict:
    res = execute_cmd_with_subprocess(f"essharp -{opt} \"{path}\"")
    if res.returncode == 0:
        return json.loads(bytes2str(res.stdout[0]))
    return {}


def get_file(fullname: str):
    path = getLocals(fullname)

    base_dir = get_base_dir(path)
    if not is_exist(base_dir):
        mkdir(base_dir)
    cd(base_dir)

    cmd = f"essharp -g \"{fullname}\" -g \"{path}\""
    execute_cmd(cmd)
