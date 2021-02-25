from enum import Flag, auto
from typing import Tuple

from PySide6 import QtGui
from PySide6.QtCore import QDir, QPointF, Slot, QSize, QPoint, QModelIndex, QAbstractItemModel
from PySide6.QtWidgets import QMainWindow, QApplication, QFileSystemModel, QStyle, QStyleFactory, QMenu
from PySide6.QtGui import QMouseEvent, QCursor, QIcon, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from util.common import get_tail

from model import EssFileModel, ItemSettingContext
from model import TreeItem
from vsstool import exec

import sys
import logging
# sys.path.extend(['/media/devecor/Data/repo/vss-cmd'])

from essexp.pyui.exp_ui import Ui_exp


class ResizeType(Flag):
    WIDTH = auto()
    HEIGHT = auto()
    BOTH = auto()
    EITHER = auto()


class MouseArea(Flag):
    RIGHT_BORDER = auto()  # right
    BOTTOM_BORDER = auto()  # bottom
    VERTEX = auto()  # diag
    INSIDE = auto()  # inner
    OUTSIDE = auto()  # out


class Exp(Ui_exp, QMainWindow):

    def __init__(self):
        super(Exp, self).__init__()
        self.setupUi(self)
        self.__start_point = QPoint()

        self.setWindowFlag(Qt.FramelessWindowHint)

        exec.execute_cmd("ss cp $/")

        ess_file_model = QStandardItemModel(1, 5)
        ess_file_model.setHorizontalHeaderLabels(["name", "date", "type", "version", "size"])

        self.__dirs_count, files_count = self.update_item_data(ItemSettingContext("$/", ess_file_model.setItem))

        self.fileTreeView.setModel(ess_file_model)

        self.resize_t = ResizeType.EITHER

        # self.setMouseTracking(True)
        # self.grabMouse()

        self.bt_close.clicked.connect(self.close)
        self.bt_maximize.clicked.connect(self.on_bt_maximize_clicked)
        self.bt_minimize.clicked.connect(self.showMinimized)
        self.fileTreeView.doubleClicked.connect(
            lambda index: self.on_item_double_clicked(index,
                                                      self.__dirs_count,
                                                      ess_file_model))
        self.fileTreeView.clicked.connect(
            lambda index: self.on_item_double_clicked(index,
                                                      self.__dirs_count,
                                                      ess_file_model))
        self.__contextMenu = QMenu(self)
        self.actionA = self.__contextMenu.addAction(u'添加')
        self.actionB = self.__contextMenu.addAction(u'删除')
        self.fileTreeView.edit = self.edit
        # self.fileTreeView.triggered.connect(self.on_item_triggered)

    def edit(self, index, trigger, event) -> bool:
        logging.debug("self.edit")
        logging.debug({
            "index": index,
            "trigger": trigger,
            "event": event
        })
        self.pos()
        return False

    def on_bt_maximize_clicked(self):
        icon = QIcon()
        if self.isMaximized():
            self.showNormal()
            icon.addFile(u":/window/jurassic_Window-max.svg", QSize(), QIcon.Normal, QIcon.Off)
        else:
            self.showMaximized()
            icon.addFile(u":/window/jurassic_Window-min.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_maximize.setIcon(icon)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        super().mouseMoveEvent(event)
        self.update_cursor(event.position())
        if event.isUpdateEvent():
            self.manual_resize(event.position())
            if self.__start_point != QPoint():
                self.move(event.globalPos() - self.__start_point)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)
        # self.releaseMouse()
        # if self.is_on_x_edge(event.position()):
        #     self.resize_t = ResizeType.WIDTH
        # elif self.is_on_y_edge(event.position()):
        #     self.resize_t = ResizeType.HEIGHT
        # elif self.is_on_diag(event.position()):
        #     self.resize_t = ResizeType.BOTH
        # else:
        #     self.resize_t = ResizeType.EITHER
        if self.is_move_area(event.position()):
            self.__start_point = event.pos()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        # self.grabMouse()
        # self.resize_t = ResizeType.EITHER
        self.__start_point = QPoint()

    def manual_resize(self, position: QPointF) -> None:
        if self.resize_t == ResizeType.WIDTH:
            self.fileTreeView.resize(position.x() - self.fileTreeView.x(),
                                     self.fileTreeView.height())
        elif self.resize_t == ResizeType.HEIGHT:
            self.fileTreeView.resize(self.fileTreeView.width(),
                                     position.y() - self.fileTreeView.y())
        elif self.resize_t == ResizeType.BOTH:
            self.fileTreeView.resize(position.x() - self.fileTreeView.x(),
                                     position.y() - self.fileTreeView.y())

    def update_cursor(self, position: QPointF):
        if self.is_on_x_edge(position):
            self.setCursor(QCursor(Qt.CursorShape.SizeHorCursor))

        elif self.is_on_y_edge(position):
            self.setCursor(QCursor(Qt.CursorShape.SizeVerCursor))

        elif self.is_on_diag(position):
            self.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))

        else:
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def is_on_x_edge(self, position: QPointF) -> bool:
        return position.y() < self.fileTreeView.geometry().bottom() - 5 and \
               self.fileTreeView.geometry().right() - 5 <= position.x() <= \
               self.fileTreeView.geometry().right() + 5

    def is_on_y_edge(self, position: QPointF) -> bool:
        return position.x() < self.fileTreeView.geometry().right() - 5 and \
               self.fileTreeView.geometry().bottom() - 5 <= position.y() <= \
               self.fileTreeView.geometry().bottom() + 5

    def is_on_diag(self, position: QPointF) -> bool:
        return self.fileTreeView.geometry().right() - 5 <= position.x() <= \
               self.fileTreeView.geometry().right() + 5 and \
               self.fileTreeView.geometry().bottom() - 5 <= position.y() <= \
               self.fileTreeView.geometry().bottom() + 5

    def is_move_area(self, position: QPointF) -> bool:
        if position.x() < self.bt_minimize.x() and position.y() < self.titlebar.geometry().bottom():
            return True
        return False

    def on_item_double_clicked(self, index: QModelIndex, dirs_count: int, model: QStandardItemModel):
        if index.row() < dirs_count:
            ancestor_indexes = [index]
            while index.parent() != QModelIndex():
                ancestor_indexes.append(index.parent())
                index = index.parent()
            ancestor_indexes.reverse()
            item = model.invisibleRootItem()
            for ancestor in ancestor_indexes:
                item = item.child(ancestor.row(), ancestor.column())
            info = {
                "accessibleText": item.accessibleText(),
                "text": item.text()
            }
            self.update_item_data(ItemSettingContext(item.accessibleText(), item.setChild))

    def update_item_data(self, context: ItemSettingContext) -> Tuple[int, int]:
        base_dir = "" if context.text() is None or context.text() == "" else context.text() + "/"
        vss_dirs = exec.list_dirs(context.text())
        for i, d in enumerate(vss_dirs):
            props = exec.get_dir_properties(base_dir + d)
            item = QStandardItem(get_tail(props[0]))
            item.setAccessibleText(props[0])
            icon = QIcon()
            icon.addFile(u":/folder/fold.svg", QSize(), QIcon.Normal, QIcon.On)
            item.setIcon(icon)
            context.set(i, 0, item)
            for j, prop in enumerate(props[1:]):
                p_item = QStandardItem(get_tail(prop))
                p_item.setAccessibleText(prop)
                context.set(i, j+1, p_item)

        vss_files = exec.list_files(context.text())
        for i, f in enumerate(vss_files):
            props = exec.get_file_properties(context.text() + "/" + f)
            for j, prop in enumerate(props):
                p_item = QStandardItem(get_tail(prop))
                p_item.setAccessibleText(prop)
                context.set(len(vss_dirs) + i, j, p_item)
        return len(vss_dirs), len(vss_files)

    def on_item_triggered(self, item: QStandardItem):
        self.__contextMenu.move(QtGui.QCursor().pos())
        self.__contextMenu.show()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication([])
    app.setStyle(QStyleFactory.create("Fusion"))
    mainWindow = Exp()
    mainWindow.show()
    sys.exit(app.exec_())
