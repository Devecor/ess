from enum import Flag, auto

from PySide6 import QtGui
from PySide6.QtCore import QPointF, QSize, QPoint
from PySide6.QtWidgets import QMainWindow, QApplication, QStyleFactory, QDialog
from PySide6.QtGui import QMouseEvent, QCursor, QIcon, QStandardItemModel
from PySide6.QtCore import Qt

from vsstool.util.common import bytes2str
from vsstool import executor

from essexp.common import get_item_by_index, ITEM_PROPERTIES, update_item_data, open_file_by_ss
from essexp.pyui.info_dialog import Ui_infoDialog
from essexp.pyui.input_dialog import Ui_inputDialog
from essexp.pyui.exp_ui import Ui_exp
from essexp.widgets.trigger_menu import TriggerMenu
from essexp.model import ItemSettingContext, EssStandardItem, EssModelIndex

import sys
import logging


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


class InfoDialog(QDialog, Ui_infoDialog):

    def __init__(self, ):
        super(InfoDialog, self).__init__()
        self.setupUi(self)


class InputDialog(QDialog, Ui_inputDialog):

    def __init__(self, ):
        super(InputDialog, self).__init__()
        self.setupUi(self)


class Exp(Ui_exp, QMainWindow):

    def __init__(self):
        super(Exp, self).__init__()
        self.setupUi(self)
        self.__start_point = QPoint()
        self.__trigger_menu = TriggerMenu(self, EssStandardItem())

        self.setWindowFlag(Qt.FramelessWindowHint)

        self.__ess_file_model = QStandardItemModel(1, len(ITEM_PROPERTIES))
        self.__ess_file_model.setHorizontalHeaderLabels(ITEM_PROPERTIES)

        self.__dirs_count = update_item_data(ItemSettingContext("$/", self.__ess_file_model.setItem))

        self.fileTreeView.setModel(self.__ess_file_model)
        # self.fileTreeView.header().setSectionResizeMode(QHeaderView.ResizeMode.Custom)
        self.fileTreeView.header().resizeSection(0, 200)

        self.resize_t = ResizeType.EITHER

        # self.setMouseTracking(True)
        # self.grabMouse()

        self.bt_close.clicked.connect(self.close)
        self.bt_maximize.clicked.connect(self.on_bt_maximize_clicked)
        self.bt_minimize.clicked.connect(self.showMinimized)
        self.fileTreeView.doubleClicked.connect(
            lambda index: self.on_item_double_clicked(index,
                                                      self.__dirs_count,
                                                      self.__ess_file_model))
        self.fileTreeView.edit = self.edit
        # self.fileTreeView.pressed.connect(self.on_item_triggered)
        self.fileTreeView.customContextMenuRequested.connect(self.on_item_triggered)

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

    def on_item_double_clicked(self, index: EssModelIndex, dirs_count: int, model: QStandardItemModel):
        item = get_item_by_index(index, model)
        if item.ss_type == "project":
            update_item_data(ItemSettingContext(item.accessibleText(), item.setChild))
        elif item.ss_type == "file":
            fullname = item.accessibleText()[:-1]
            open_file_by_ss(fullname, item.ss_timestamp)

    def on_item_triggered(self, pos: QPoint):
        logging.debug("self.on_item_triggered")
        index = self.fileTreeView.indexAt(pos)
        if index == EssModelIndex():
            return
        item = get_item_by_index(index.sibling(index.row(), 0), self.__ess_file_model)
        self.__trigger_menu = TriggerMenu(self, item)
        if item.ss_type == "project":
            self.__trigger_menu.enable_slots(rename=self.rename)
        elif item.ss_type == "file":
            self.__trigger_menu.enable_slots(checkout=self.try_checkout,
                                             checkin=self.try_checkin,
                                             uncheckout=self.try_uncheckout,
                                             stage=self.testttt,
                                             rename=self.rename)
        else:
            logging.error("inner essexp exception occurring!!!")
            raise RuntimeError()
        self.__trigger_menu.move(QtGui.QCursor().pos())
        self.__trigger_menu.show()

    def __update_file_status(self, item: EssStandardItem):
        stat = executor.execute_cmd_with_subprocess(f"ss status \"{item.accessibleText()}\"").stdout[0]
        stat = bytes2str(stat).split()
        exc_i = [i for i in range(len(stat)) if stat[i] == 'Exc'][0]
        name_col = self.__ess_file_model.item(item.row(), 5)
        date_col = self.__ess_file_model.item(item.row(), 1)
        fold_col = self.__ess_file_model.item(item.row(), 6)
        name_col.setText(stat[exc_i - 1])
        date_col.setText(stat[exc_i + 1] + "   " + stat[exc_i + 2])
        fold_col.setText(stat[-1])

    def try_checkout(self):
        item = self.__trigger_menu.item
        res = executor.execute_cmd_with_subprocess(f"ss checkout \"{item.accessibleText()}\"")
        if res.returncode != 0:
            info_dialog = InfoDialog()
            info_dialog.textLabel.setText("已被签出/签出失败")
            info_dialog.show()
            info_dialog.exec_()
            return
        self.__update_file_status(item)

    def try_checkin(self):
        item = self.__trigger_menu.item
        res = executor.execute_cmd_with_subprocess(f"ss checkin \"{item.accessibleText()}\"")
        if res.returncode != 0:
            info_dialog = InfoDialog()
            info_dialog.textLabel.setText("签入失败")
            info_dialog.show()
            info_dialog.exec_()
        self.__update_file_status(item)

    def try_uncheckout(self):
        item = self.__trigger_menu.item
        res = executor.execute_cmd_with_subprocess(f"ss undocheckout \"{item.accessibleText()}\"")
        if res.returncode != 0:
            info_dialog = InfoDialog()
            info_dialog.textLabel.setText("取消签出失败")
            info_dialog.show()
            info_dialog.exec_()
        self.__update_file_status(item)

    def rename(self):
        item = self.__trigger_menu.item
        input_dialog = InputDialog()
        input_dialog.le_input.setPlaceholderText("filename")
        input_dialog.show()
        input_dialog.exec_()
        res = executor.execute_cmd_with_subprocess(
            f"ss rename \"{item.accessibleText()}\" \"{input_dialog.le_input.text()}\"")
        if res.returncode != 0:
            info_dialog = InfoDialog()
            info_dialog.textLabel.setText("重命名失败")
            info_dialog.show()
            info_dialog.exec_()
        else:
            item_base_dirs = item.accessibleText().split("/")[:-1]
            item_base_dirs.append(input_dialog.le_input.text())
            item.setAccessibleText("/".join(item_base_dirs))
            item.setText(input_dialog.le_input.text())
            self.__update_file_status(item)

    def testttt(self):
        pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication([])
    app.setStyle(QStyleFactory.create("Fusion"))
    mainWindow = Exp()
    mainWindow.show()
    sys.exit(app.exec_())
