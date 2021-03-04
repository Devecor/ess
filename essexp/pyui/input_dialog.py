# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'input_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.0.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_inputDialog(object):
    def setupUi(self, inputDialog):
        if not inputDialog.objectName():
            inputDialog.setObjectName(u"inputDialog")
        inputDialog.resize(400, 100)
        self.horizontalLayout = QHBoxLayout(inputDialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.le_input = QLineEdit(inputDialog)
        self.le_input.setObjectName(u"le_input")

        self.verticalLayout.addWidget(self.le_input)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.buttonBox = QDialogButtonBox(inputDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.retranslateUi(inputDialog)
        self.buttonBox.accepted.connect(inputDialog.accept)
        self.buttonBox.rejected.connect(inputDialog.reject)

        QMetaObject.connectSlotsByName(inputDialog)
    # setupUi

    def retranslateUi(self, inputDialog):
        inputDialog.setWindowTitle(QCoreApplication.translate("inputDialog", u"Dialog", None))
    # retranslateUi

