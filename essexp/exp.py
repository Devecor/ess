from enum import Flag, auto
from PySide6 import QtGui
from PySide6.QtCore import QSize, QPoint
from PySide6.QtWidgets import QMainWindow, QApplication, QStyleFactory, QDialog
from PySide6.QtGui import QIcon, QStandardItemModel, QBrush, QColor
from PySide6.QtCore import Qt

from vsstool.util.cmd import mkdir, cd
from vsstool.util.common import get_base_dir, is_exist, open_file, get_tail
from vsstool import executor

from essexp.common import get_item_by_index, ITEM_PROPERTIES, update_item_data, open_file_by_ss, set_icon, \
    get_from_essharp, get_file, update_item_data_on_error
from essexp.pyui.info_dialog import Ui_infoDialog
from essexp.pyui.input_dialog import Ui_inputDialog
from essexp.pyui.exp_ui import Ui_exp
from essexp.widgets.trigger_menu import TriggerMenu
from essexp.model import ItemSettingContext, EssStandardItem, EssModelIndex

import sys
import logging

from vsstool.util.config import getLocals
import pyperclip


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
        self.option = "rejected"
        self.buttonBox.accepted.connect(self.set_accept)

    def set_accept(self) -> None:
        self.option = "accepted"


class Exp(Ui_exp, QMainWindow):

    def __init__(self):
        super(Exp, self).__init__()
        self.setupUi(self)
        self.__last_pos = self.pos()
        self.__trigger_menu = TriggerMenu(self, EssStandardItem())
        self.__cur_parent = EssStandardItem()

        self.setWindowFlag(Qt.FramelessWindowHint)

        self.__ess_file_model = QStandardItemModel(1, len(ITEM_PROPERTIES))
        self.__ess_file_model.setHorizontalHeaderLabels(ITEM_PROPERTIES)

        update_item_data(ItemSettingContext("$/", self.__ess_file_model.setItem))

        self.fileTreeView.setModel(self.__ess_file_model)
        self.fileTreeView.header().resizeSection(0, 300)
        self.fileTreeView.header().resizeSection(1, 120)

        self.resize_t = ResizeType.EITHER

        self.bt_close.clicked.connect(self.close)
        self.bt_copy.clicked.connect(self.on_copy_button_clicked)
        self.bt_copy.mouseDoubleClickEvent = self.on_copy_button_double_clicked

        self.bt_maximize.clicked.connect(self.on_bt_maximize_clicked)
        self.bt_minimize.clicked.connect(self.showMinimized)

        self.fileTreeView.doubleClicked.connect(self.on_item_double_clicked)
        self.fileTreeView.clicked.connect(self.on_item_clicked)
        self.fileTreeView.edit = self.edit
        self.fileTreeView.customContextMenuRequested.connect(self.on_item_triggered)

        self.lb_cpath.setText("$/")

    def edit(self, index, trigger, event) -> bool:
        """禁止edit"""
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

    def on_error(self):
        self.__cur_parent.removeRows(0, self.__cur_parent.rowCount())
        update_item_data_on_error(ItemSettingContext(self.__cur_parent.accessibleText(),
                                                     self.__cur_parent.setChild))

    def on_item_double_clicked(self, index: EssModelIndex):
        item = get_item_by_index(index, self.__ess_file_model)
        self.__cur_parent = item
        if item.ss_type == "project":
            item.removeRows(0, item.rowCount())
            update_item_data(ItemSettingContext(item.accessibleText(), item.setChild, self.on_error))
        elif item.ss_type == "file":
            fullname = item.accessibleText()
            if item.ss_cho:
                open_res = open_file_by_ss(fullname, override=False)
            else:
                open_res = open_file_by_ss(fullname, override=True)

            if not open_res:
                info_dialog = InfoDialog()
                info_dialog.textLabel.setText("打开失败")
                info_dialog.show()
                info_dialog.exec_()

    def on_item_clicked(self, index: EssModelIndex):
        item = get_item_by_index(index, self.__ess_file_model)
        if item.ss_type == "project":
            self.lb_cpath.setText(item.accessibleText())
        elif item.ss_type == "file":
            self.lb_cpath.setText(item.accessibleText())
            self.__update_file_status(item)

    def on_copy_button_clicked(self):
        pyperclip.copy(self.lb_cpath.text())

    def on_copy_button_double_clicked(self, event):
        name = self.lb_cpath.text()
        if name.endswith("/"):
            name = name[:-1]
        pyperclip.copy(get_tail(name))

    def on_item_triggered(self, pos: QPoint):
        index = self.fileTreeView.indexAt(pos)
        if index == EssModelIndex():
            return
        item = get_item_by_index(index.sibling(index.row(), 0), self.__ess_file_model)
        self.__trigger_menu = TriggerMenu(self, item)
        if item.ss_type == "project":
            self.__trigger_menu.enable_slots(open_in_folder=self.open_in_folder,
                                             rename=self.rename, )
        elif item.ss_type == "file":
            self.__trigger_menu.enable_slots(open_in_folder=self.open_in_folder,
                                             edit=self.try_edit,
                                             checkout=self.try_checkout,
                                             checkin=self.try_checkin,
                                             uncheckout=self.try_uncheckout,
                                             rename=self.rename, )
        else:
            raise RuntimeError()
        self.__trigger_menu.move(QtGui.QCursor().pos())
        self.__trigger_menu.show()

    def __update_file_status(self, item: EssStandardItem):
        stat = get_from_essharp(item.accessibleText(), "s")
        if not len(stat):
            logging.error("get_from_essharp fail: " + item.accessibleText())
            return
        parent = item.parent()
        if parent is None:
            name_col = self.__ess_file_model.item(item.row(), ITEM_PROPERTIES.index("user"))
            date_col = self.__ess_file_model.item(item.row(), ITEM_PROPERTIES.index("date"))
        else:
            name_col = parent.child(item.row(), ITEM_PROPERTIES.index("user"))
            date_col = parent.child(item.row(), ITEM_PROPERTIES.index("date"))

        if stat["ischeckout"]:
            name_col.setText(stat["checkout_info"]["user_name"])
            date_col.setText(stat["checkout_info"]["date"])
            item.setForeground(QBrush(QColor("red")))
            set_icon(item, u":/checkout/checkoutline02.svg")
        else:
            name_col.setText(stat["version_info"]["user_name"])
            date_col.setText(stat["version_info"]["date"])
            item.setForeground(QBrush(QColor("black")))
            set_icon(item, u":/file/file.svg")

    def try_checkout(self) -> bool:
        item = self.__trigger_menu.item
        res = executor.execute_cmd_with_subprocess(f"ss checkout \"{item.accessibleText()}\"")
        if res.returncode != 0:
            info_dialog = InfoDialog()
            info_dialog.textLabel.setText("已被签出/签出失败")
            info_dialog.show()
            info_dialog.exec_()
            return False
        self.__update_file_status(item)
        return True

    def try_edit(self):
        if not self.try_checkout():
            return
        item = self.__trigger_menu.item
        if not open_file_by_ss(item.accessibleText(), override=True):
            info_dialog = InfoDialog()
            info_dialog.textLabel.setText("打开失败")
            info_dialog.show()
            info_dialog.exec_()

    def try_checkin(self):
        item = self.__trigger_menu.item
        res = executor.execute_cmd_with_subprocess(f"ss checkin \"{item.accessibleText()}\" -c-")
        if res.returncode != 0:
            info_dialog = InfoDialog()
            info_dialog.textLabel.setText("签入失败")
            info_dialog.show()
            info_dialog.exec_()
            return
        self.__update_file_status(item)

    def try_uncheckout(self):
        item = self.__trigger_menu.item
        get_file(item.accessibleText())
        res = executor.execute_cmd_with_subprocess(f"ss undocheckout \"{item.accessibleText()}\" -i-")
        if res.returncode != 0:
            info_dialog = InfoDialog()
            info_dialog.textLabel.setText("取消签出失败")
            info_dialog.show()
            info_dialog.exec_()
            return
        self.__update_file_status(item)

    def rename(self):
        item = self.__trigger_menu.item
        input_dialog = InputDialog()
        input_dialog.le_input.setText(item.text())
        input_dialog.show()
        input_dialog.exec_()

        if input_dialog.option == "rejected" or input_dialog.le_input.text() == "":
            return
        name = get_base_dir(item.accessibleText()[:-1]) + "/" + input_dialog.le_input.text()
        res = executor.execute_cmd_with_subprocess(
            f"ss rename \"{item.accessibleText()}\" \"{name}\"")
        if res.returncode != 0:
            info_dialog = InfoDialog()
            info_dialog.textLabel.setText("重命名失败")
            info_dialog.show()
            info_dialog.exec_()
        else:
            item.setAccessibleText(name)
            item.setText(input_dialog.le_input.text())
            if item.ss_type == "file":
                self.__update_file_status(item)

    def open_in_folder(self):
        item = self.__trigger_menu.item
        local = getLocals(item.accessibleText())
        if item.ss_type == 'project':
            base_dir = local
        else:
            base_dir = get_base_dir(local)

        if not is_exist(base_dir):
            mkdir(base_dir)
        cd(base_dir)
        if item.ss_type == 'file':
            if not is_exist(local):
                get_file(item.accessibleText())

        open_file(base_dir)
        if item.ss_type == 'project':
            open_file('cmd')

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.__last_pos = event.globalPos()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        dx = event.globalX() - self.__last_pos.x()
        dy = event.globalY() - self.__last_pos.y()
        self.__last_pos = event.globalPos()
        self.move(self.x() + dx, self.y() + dy)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication([])
    app.setStyle(QStyleFactory.create("Fusion"))
    mainWindow = Exp()
    mainWindow.show()
    sys.exit(app.exec_())
