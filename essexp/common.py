from typing import Tuple

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QStandardItemModel
from vsstool.util.common import get_tail

from essexp.model import ItemSettingContext, EssStandardItem, EssModelIndex
from vsstool import executor

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


def update_item_data(context: ItemSettingContext) -> Tuple[int, int]:
    base_dir = "" if context.text() is None or context.text() == "" else context.text() + "/"

    vss_dirs = executor.list_dirs(context.text())
    for i, d in enumerate(vss_dirs):
        props = executor.get_dir_properties(base_dir + d)
        props.extend(["" for _ in range(len(ITEM_PROPERTIES) - len(props))])
        item_i = EssStandardItem(get_tail(props[0]))
        item_i.ss_type = "dir"
        item_i.setAccessibleText(props[0])
        set_icon(item_i, u":/folder/fold.svg")
        context.set(i, 0, item_i)

        for j, prop in enumerate(props[1:]):
            item_j = EssStandardItem(prop)
            item_j.ss_type = ITEM_PROPERTIES[j+1]
            item_j.setAccessibleText(prop)
            context.set(i, j+1, item_j)

    vss_files = executor.list_files(context.text())
    for i, f in enumerate(vss_files):
        props = executor.get_file_properties(context.text() + ("" if context.text().endswith("/") else "/") + f)
        props.extend(["" for _ in range(len(ITEM_PROPERTIES) - len(props))])
        item_i = EssStandardItem(get_tail(props[0]))
        item_i.ss_type = "file"
        item_i.setAccessibleText(props[0])
        # set_icon(item_i, u":/folder/fold.svg")
        context.set(len(vss_dirs) + i, 0, item_i)

        for j, prop in enumerate(props[1:]):
            item_j = EssStandardItem(prop)
            item_j.ss_type = ITEM_PROPERTIES[j + 1]
            item_j.setAccessibleText(prop)
            context.set(len(vss_dirs) + i, j+1, item_j)
    return len(vss_dirs), len(vss_files)
