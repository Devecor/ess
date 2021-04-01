from typing import Tuple, List

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QStandardItemModel

from vsstool.executor import get_items, sync_dir
from vsstool.util.cmd import mkdir, cd
from vsstool.util.common import get_tail, get_base_dir, is_exist, execute_cmd, open_file, get_file_timestamp

from essexp.model import ItemSettingContext, EssStandardItem, EssModelIndex
from vsstool import executor
import threading

from vsstool.util.config import getLocals

ITEM_PROPERTIES = ["name", "date", "type", "version", "size", "user", "checkout folder"]


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
    items = get_items(context.text())
    for i, d in enumerate(items.keys()):
        item_i = EssStandardItem(d)
        item_i.ss_type = items[d]["type"]
        item_i.ss_timestamp = items[d]["version_info"]["date"]

        props = [
            items[d]["version_info"]["date"],
            items[d]["type"],
            items[d]["version_number"],
            items[d]["size"],
            items[d]["version_info"]["user_name"],
            ""
        ]

        if items[d]["type"] == "project":
            set_icon(item_i, u":/folder/fold.svg")
            item_i.setAccessibleText(context.text() + d + "/")
        else:
            item_i.setAccessibleText(context.text() + d)
            if items[d]["ischeckout"]:
                set_icon(item_i, u":/checkout/checkoutline02.svg")
                props[-1] = get_base_dir(items[d]["local_space"])
        context.set(i, 0, item_i)

        for j, prop in enumerate(props):
            item_j = EssStandardItem(str(prop))
            item_j.ss_type = ITEM_PROPERTIES[j + 1]
            context.set(i, j + 1, item_j)


def update_dirs(base_dir: str, context: ItemSettingContext):
    vss_dirs = executor.list_dirs(context.text())
    for i, d in enumerate(vss_dirs):
        item_i = EssStandardItem(d)
        item_i.ss_type = "project"
        set_icon(item_i, u":/folder/fold.svg")
        context.set(i, 0, item_i)
        threading.Thread(target=executor.get_dir_properties,
                         args=(base_dir + d, on_dir_properties_owned, item_i, i, context)).start()
    return len(vss_dirs)


def update_files(dirs_count: int, context: ItemSettingContext):
    vss_files = executor.list_files(context.text())
    for i, f in enumerate(vss_files):
        item_i = EssStandardItem(f)
        item_i.ss_type = "file"
        context.set(dirs_count + i, 0, item_i)
        threading.Thread(target=executor.get_file_properties,
                         args=(
                             context.text() + ("" if context.text().endswith("/") else "/") + f,
                             on_file_properties_owned,
                             item_i,
                             i,
                             context
                         )).start()

    return len(vss_files)


def on_dir_properties_owned(props, item: EssStandardItem, row, context):
    props.extend(["" for _ in range(len(ITEM_PROPERTIES) - len(props))])
    item.setAccessibleText(props[0])

    for j, prop in enumerate(props[1:]):
        item_j = EssStandardItem(prop)
        item_j.ss_type = ITEM_PROPERTIES[j + 1]
        item_j.setAccessibleText(prop)
        context.set(row, j + 1, item_j)


def on_file_properties_owned(props, item: EssStandardItem, row, context, dirs_count):
    props.extend(["" for _ in range(len(ITEM_PROPERTIES) - len(props))])
    item.setAccessibleText(props[0])
    # set_icon(item_i, u":/folder/fold.svg")
    for j, prop in enumerate(props[1:]):
        item_j = EssStandardItem(prop)
        item_j.ss_type = ITEM_PROPERTIES[j + 1]
        item_j.setAccessibleText(prop)
        context.set(dirs_count + row, j + 1, item_j)


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
