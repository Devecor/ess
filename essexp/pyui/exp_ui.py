# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'exp.ui'
##
## Created by: Qt User Interface Compiler version 6.0.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import icon_rc

class Ui_exp(object):
    def setupUi(self, exp):
        if not exp.objectName():
            exp.setObjectName(u"exp")
        exp.setWindowModality(Qt.ApplicationModal)
        exp.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(exp.sizePolicy().hasHeightForWidth())
        exp.setSizePolicy(sizePolicy)
        exp.setContextMenuPolicy(Qt.DefaultContextMenu)
        icon = QIcon()
        icon.addFile(u":/logo/logo-polymer.svg", QSize(), QIcon.Normal, QIcon.Off)
        exp.setWindowIcon(icon)
        self.centralwidget = QWidget(exp)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.titlebar = QFrame(self.centralwidget)
        self.titlebar.setObjectName(u"titlebar")
        sizePolicy1.setHeightForWidth(self.titlebar.sizePolicy().hasHeightForWidth())
        self.titlebar.setSizePolicy(sizePolicy1)
        self.titlebar.setMinimumSize(QSize(0, 30))
        self.titlebar.setMaximumSize(QSize(16777215, 40))
        self.titlebar.setMouseTracking(True)
        self.titlebar.setStyleSheet(u"QPushButton{\n"
"    background: rgba(0,0,0,0);\n"
"    border: 0px;\n"
"}")
        self.horizontalLayout = QHBoxLayout(self.titlebar)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(2, 2, 4, 4)
        self.bt_logo = QPushButton(self.titlebar)
        self.bt_logo.setObjectName(u"bt_logo")
        self.bt_logo.setMinimumSize(QSize(32, 32))
        self.bt_logo.setMaximumSize(QSize(32, 32))
        self.bt_logo.setAutoFillBackground(False)
        self.bt_logo.setStyleSheet(u"")
        self.bt_logo.setIcon(icon)
        self.bt_logo.setIconSize(QSize(32, 32))
        self.bt_logo.setAutoRepeatDelay(0)
        self.bt_logo.setAutoRepeatInterval(0)
        self.bt_logo.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.bt_logo)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.lb_title = QLabel(self.titlebar)
        self.lb_title.setObjectName(u"lb_title")
        self.lb_title.setMaximumSize(QSize(512, 16777215))
        font = QFont()
        font.setPointSize(16)
        self.lb_title.setFont(font)
        self.lb_title.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.lb_title)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.bt_minimize = QPushButton(self.titlebar)
        self.bt_minimize.setObjectName(u"bt_minimize")
        sizePolicy1.setHeightForWidth(self.bt_minimize.sizePolicy().hasHeightForWidth())
        self.bt_minimize.setSizePolicy(sizePolicy1)
        self.bt_minimize.setMinimumSize(QSize(24, 24))
        self.bt_minimize.setMaximumSize(QSize(32, 32))
        icon1 = QIcon()
        icon1.addFile(u":/window/jurassic_delete.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_minimize.setIcon(icon1)
        self.bt_minimize.setIconSize(QSize(24, 24))
        self.bt_minimize.setAutoRepeatDelay(0)
        self.bt_minimize.setAutoRepeatInterval(0)
        self.bt_minimize.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.bt_minimize)

        self.bt_maximize = QPushButton(self.titlebar)
        self.bt_maximize.setObjectName(u"bt_maximize")
        self.bt_maximize.setMinimumSize(QSize(24, 24))
        self.bt_maximize.setMaximumSize(QSize(32, 32))
        icon2 = QIcon()
        icon2.addFile(u":/window/jurassic_Window-max.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_maximize.setIcon(icon2)
        self.bt_maximize.setIconSize(QSize(24, 24))
        self.bt_maximize.setAutoRepeatDelay(0)
        self.bt_maximize.setAutoRepeatInterval(0)
        self.bt_maximize.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.bt_maximize)

        self.bt_close = QPushButton(self.titlebar)
        self.bt_close.setObjectName(u"bt_close")
        self.bt_close.setMinimumSize(QSize(24, 24))
        self.bt_close.setMaximumSize(QSize(32, 32))
        icon3 = QIcon()
        icon3.addFile(u":/close/jurassic_close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_close.setIcon(icon3)
        self.bt_close.setIconSize(QSize(24, 24))
        self.bt_close.setAutoRepeatDelay(0)
        self.bt_close.setAutoRepeatInterval(0)
        self.bt_close.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.bt_close)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 1)
        self.horizontalLayout.setStretch(5, 1)
        self.horizontalLayout.setStretch(6, 1)

        self.verticalLayout.addWidget(self.titlebar)

        self.fileTreeView = QTreeView(self.centralwidget)
        self.fileTreeView.setObjectName(u"fileTreeView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.fileTreeView.sizePolicy().hasHeightForWidth())
        self.fileTreeView.setSizePolicy(sizePolicy2)
        self.fileTreeView.setMinimumSize(QSize(0, 256))
        self.fileTreeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.fileTreeView.setTextElideMode(Qt.ElideRight)
        self.fileTreeView.setAutoExpandDelay(0)
        self.fileTreeView.setIndentation(20)
        self.fileTreeView.setItemsExpandable(True)
        self.fileTreeView.setExpandsOnDoubleClick(True)
        self.fileTreeView.header().setCascadingSectionResizes(True)
        self.fileTreeView.header().setDefaultSectionSize(60)

        self.verticalLayout.addWidget(self.fileTreeView)

        exp.setCentralWidget(self.centralwidget)

        self.retranslateUi(exp)
        self.bt_close.clicked.connect(exp.close)

        QMetaObject.connectSlotsByName(exp)
    # setupUi

    def retranslateUi(self, exp):
        exp.setWindowTitle(QCoreApplication.translate("exp", u"ess", None))
        self.bt_logo.setText("")
        self.lb_title.setText(QCoreApplication.translate("exp", u"ess explorer", None))
        self.bt_minimize.setText("")
        self.bt_maximize.setText("")
        self.bt_close.setText("")
    # retranslateUi

