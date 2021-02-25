import typing
from PySide6.QtCore import QAbstractItemModel, QModelIndex, Qt
import logging

from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QFileSystemModel


class TreeItem(object):
    def __init__(self, data: typing.List[typing.Any], parent_item=None):
        self.__item_data = data
        self.__parent_item = parent_item
        self.__child_items = []

    def child(self, row: int):
        if row < 0 or row >= len(self.__item_data):
            return None
        return self.__child_items[row]

    def child_count(self):
        return len(self.__child_items)

    def get_row(self, ins):
        return self.__child_items.index(ins)

    def append_child(self, child):
        self.__child_items.append(child)

    def child_number(self) -> int:
        if self.__parent_item:
            logging.debug({
                "TreeItem -> child_number -> return": self.__parent_item.get_row(self)
            })
            return self.__parent_item.get_row(self)
        return 0

    def column_count(self):
        return len(self.__item_data)

    def data(self, column: int):
        if column < 0 or column >= len(self.__item_data):
            return None
        return self.__item_data[column]

    def insert_children(self, position: int, columns: int):
        if position < 0 or position > len(self.__child_items):
            return False
        self.__child_items.insert(position, TreeItem([], None))
        return True

    def insert_columns(self, position: int, columns: int):
        if position < 0 or position > len(self.__item_data):
            return False
        for _ in range(columns):
            self.__item_data.insert(position, None)
        for child in self.__child_items:
            child.insert_columns(position, columns)
        return True

    def parent(self):
        return self.__parent_item

    def remove_children(self, position: int, count: int) -> bool:
        if position < 0 or position + count > len(self.__child_items):
            return False
        for  _ in range(count):
            self.__child_items.pop(position)
        return True

    def remove_columns(self, position: int, columns: int) -> bool:
        if position < 0 or position + columns > len(self.__item_data):
            return False
        for _ in range(columns):
            self.__item_data.pop(position)
        for child in self.__child_items:
            child.remove_columns(position, columns)
        return True

    def set_data(self, column: int, value) -> bool:
        if column < 0 or column >= len(self.__item_data):
            return False
        self.__item_data[column] = value
        return True


class TreeModel(QStandardItemModel):
    def __init__(self):
        super().__init__()


class ItemSettingContext(object):
    def __init__(self, origin: str, setter: typing.Callable):
        self.__f = setter
        self.__origin = origin

    def set(self, row: int, col: int, item: QStandardItem):
        self.__f(row, col, item)

    def text(self):
        return self.__origin


class EssFileModel(QAbstractItemModel):

    def __init__(self, parent):
        super().__init__()
        self.__root = parent

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        index_arg_in = {"row": row,
                        "column": column,
                        "parent": parent}
        logging.debug("index")
        logging.debug(index_arg_in)
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        if not parent.isValid():
            parent_item = self.__root
        else:
            parent_item = parent.internalPointer()
        res = parent_item.child(row)
        if res is None:
            return QModelIndex()
        logging.debug({"return": self.createIndex(row, column, res)})
        return self.createIndex(row, column, res)

    def parent(self, child: QModelIndex = ...) -> QModelIndex:
        parent_arg_in = {"child": child}
        logging.debug("parent")
        logging.debug(parent_arg_in)
        if not child.isValid():
            return QModelIndex()
        child_item = child.internalPointer()
        parent_item = child_item.parent_item()
        if parent_item == self.__root:
            return QModelIndex()
        logging.debug({"return": self.createIndex(parent_item.row(), 0, parent_item)})
        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        row_count_arg_in = {"parent": parent}
        logging.debug("rowCount")
        logging.debug(row_count_arg_in)
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item = self.__root
        else:
            parent_item = parent.internalPointer()
        logging.debug({"return": parent_item.child_count()})
        return parent_item.child_count()

    def columnCount(self, parent: QModelIndex = ...) -> int:
        column_count_arg_in = {"parent": parent}
        logging.debug("columnCount")
        logging.debug(column_count_arg_in)
        if parent.isValid():
            logging.debug({"return": parent.internalPointer().column_count()})
            return parent.internalPointer().column_count()
        logging.debug({"return": self.__root.column_count()})
        return self.__root.column_count()

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        data_arg_in = {
            "index": index,
            "role": role
        }
        logging.debug(data_arg_in)
        if not index.isValid():
            return None
        r = int(Qt.DisplayRole)
        c = index.column()
        if role != Qt.DisplayRole:
            val = index.internalPointer().data(index.column())
            return None

        return index.internalPointer().data(index.column())

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags
        return super().flags(index)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        header_data = {
            "section": section,
            "orientation": orientation,
            "role": role
        }
        logging.debug("headerData")
        logging.debug(header_data)
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.__root.data(section)
        return None
