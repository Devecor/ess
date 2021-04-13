import json

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QStandardItemModel

from vsstool.util.cmd import mkdir, cd
from vsstool.util.common import get_base_dir, is_exist, execute_cmd, open_file, get_file_timestamp, \
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


def update_item_data(context: ItemSettingContext):
    items = get_from_essharp(context.text(), "n")
    for i, d in enumerate(items.keys()):
        item_i = EssStandardItem(d)
        item_i.ss_type = items[d].get("type")

        if items[d].get("type") == "project":
            set_icon(item_i, u":/folder/fold.svg")
            item_i.setAccessibleText(context.text() + d + "/")
        else:
            item_i.setAccessibleText(context.text() + d)
            if items[d].get("ischeckout"):
                set_icon(item_i, u":/checkout/checkoutline02.svg")
            else:
                set_icon(item_i, u":/file/file.svg")
        context.set(i, 0, item_i)

        for j, t in enumerate(ITEM_PROPERTIES[1:]):
            item_j = EssStandardItem("")
            item_j.ss_type = t
            context.set(i, j + 1, item_j)

        threading.Thread(target=update_item_props,
                         args=(context.text() + d, i, context)).start()


def update_item_props(path: str, row, context):
    vss_res = get_from_essharp(path, "d")
    props = [
        vss_res["version_info"]["date"],
        vss_res["type"],
        vss_res["version_number"],
        vss_res["size"],
        vss_res["version_info"]["user_name"],
    ]
    for j, d in enumerate(props):
        item_j = EssStandardItem(str(d))
        item_j.ss_type = ITEM_PROPERTIES[j+1]
        context.set(row, j + 1, item_j)


def open_file_by_ss(fullname: str) -> bool:
    path = getLocals(fullname)

    base_dir = get_base_dir(path)
    if not is_exist(base_dir):
        mkdir(base_dir)
    cd(base_dir)

    cmd = f"ss get \"{fullname}\""
    execute_cmd(cmd)

    if is_exist(path):
        open_file(path)
        return True


def get_from_essharp(path, opt) -> dict:
    res = execute_cmd_with_subprocess(f"essharp -{opt} \"{path}\"")
    if res.returncode == 0:
        return json.loads(bytes2str(res.stdout[0]))
    return {}
