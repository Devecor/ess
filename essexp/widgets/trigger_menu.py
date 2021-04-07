import logging
from typing import Callable

from PySide6.QtGui import QStandardItem
from PySide6.QtWidgets import QMenu, QWidget


class TriggerMenu(QMenu):
    def __init__(self, context: QWidget, item: QStandardItem):
        super().__init__(context)
        self.__item = item

    def enable_slots(self, **kwargs):
        logging.debug(kwargs)
        for i in kwargs.keys():
            self.addAction(i.replace("_", " ")).triggered.connect(kwargs[i])

    @property
    def item(self):
        return self.__item


def triggered(ins: TriggerMenu):
    def decorator(f: Callable):
        def wrapper(*args, **kwargs):
            item = ins.item
            info = {
                "row": item.row(),
                "col": item.column(),
                "accessibleText": item.accessibleText(),
                "text": item.text()
            }
            return f(ins.item, *args, **kwargs)
        return wrapper
    return decorator
