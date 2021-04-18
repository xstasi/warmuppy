# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
##
## Created by: Qt User Interface Compiler version 6.0.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_About(object):
    def setupUi(self, About):
        if not About.objectName():
            About.setObjectName(u"About")
        About.resize(248, 174)
        self.verticalLayout = QVBoxLayout(About)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelNameVersion = QLabel(About)
        self.labelNameVersion.setObjectName(u"labelNameVersion")

        self.verticalLayout.addWidget(self.labelNameVersion)

        self.line = QFrame(About)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.label = QLabel(About)
        self.label.setObjectName(u"label")
        self.label.setAutoFillBackground(False)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(About)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(About)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.pushButton = QPushButton(About)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(About)

        QMetaObject.connectSlotsByName(About)
    # setupUi

    def retranslateUi(self, About):
        About.setWindowTitle(QCoreApplication.translate("About", u"About Warmuppy", None))
        self.labelNameVersion.setText(QCoreApplication.translate("About", u"<name version>", None))
        self.label.setText(QCoreApplication.translate("About", u"Warmuppy is a helper to practice vocal warm-up exercises.", None))
        self.label_2.setText(QCoreApplication.translate("About", u"Written by Alessandro Grassi.", None))
        self.label_3.setText(QCoreApplication.translate("About", u"Licensed under the EUPL, version 1.2.", None))
        self.pushButton.setText(QCoreApplication.translate("About", u"OK", None))
    # retranslateUi

