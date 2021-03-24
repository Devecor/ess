from typing import Tuple, List

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QStandardItemModel
from vsstool.util.common import get_tail

from essexp.model import ItemSettingContext, EssStandardItem, EssModelIndex
from vsstool import executor
import threading

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


def update_item_data(context: ItemSettingContext) -> int:
    base_dir = "" if context.text() is None or context.text() == "" else context.text() + "/"

    dirs_count = update_dirs(base_dir, context)
    update_files(dirs_count, context)

    return dirs_count


def update_dirs(base_dir: str, context: ItemSettingContext):
    vss_dirs = executor.list_dirs(context.text())
    for i, d in enumerate(vss_dirs):
        item_i = EssStandardItem(d)
        item_i.ss_type = "dir"
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
