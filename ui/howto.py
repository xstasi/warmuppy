# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'howto.ui'
##
## Created by: Qt User Interface Compiler version 6.0.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Howto(object):
    def setupUi(self, Howto):
        if not Howto.objectName():
            Howto.setObjectName(u"Howto")
        Howto.resize(382, 198)
        self.gridLayout = QGridLayout(Howto)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Howto)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.line = QFrame(Howto)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.label_2 = QLabel(Howto)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_2)

        self.line_2 = QFrame(Howto)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.label_3 = QLabel(Howto)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(Howto)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(Howto)

        QMetaObject.connectSlotsByName(Howto)
    # setupUi

    def retranslateUi(self, Howto):
        Howto.setWindowTitle(QCoreApplication.translate("Howto", u"How to use Warmuppy", None))
        self.label.setText(QCoreApplication.translate("Howto", u"Choose a starting point for your exercise by selecting a note and an octave.", None))
        self.label_2.setText(QCoreApplication.translate("Howto", u"Use Play/Stop to start or stop the exercise, Higher/Lower to increase or decrease the starting note.", None))
        self.label_3.setText(QCoreApplication.translate("Howto", u"Step controls the amount of semitones increased or decreased by the Higher/Lower buttons. BPM controls the exercise speed. Cut controls the amount of silence inserted at the end of each note.", None))
        self.pushButton.setText(QCoreApplication.translate("Howto", u"OK", None))
    # retranslateUi

