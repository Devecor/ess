# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'info_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.0.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_infoDialog(object):
    def setupUi(self, infoDialog):
        if not infoDialog.objectName():
            infoDialog.setObjectName(u"infoDialog")
        infoDialog.resize(400, 300)
        infoDialog.setStyleSheet(u"")
        infoDialog.setModal(False)
        self.verticalLayout = QVBoxLayout(infoDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textLabel = QLabel(infoDialog)
        self.textLabel.setObjectName(u"textLabel")
        self.textLabel.setMinimumSize(QSize(0, 200))
        self.textLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.textLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.bt_ensure = QPushButton(infoDialog)
        self.bt_ensure.setObjectName(u"bt_ensure")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_ensure.sizePolicy().hasHeightForWidth())
        self.bt_ensure.setSizePolicy(sizePolicy)
        self.bt_ensure.setMinimumSize(QSize(300, 30))
        font = QFont()
        font.setPointSize(11)
        self.bt_ensure.setFont(font)

        self.horizontalLayout.addWidget(self.bt_ensure)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(infoDialog)
        self.bt_ensure.clicked.connect(infoDialog.close)

        QMetaObject.connectSlotsByName(infoDialog)
    # setupUi

    def retranslateUi(self, infoDialog):
        infoDialog.setWindowTitle(QCoreApplication.translate("infoDialog", u"Dialog", None))
        self.textLabel.setText("")
        self.bt_ensure.setText(QCoreApplication.translate("infoDialog", u"\u786e\u5b9a", None))
    # retranslateUi

