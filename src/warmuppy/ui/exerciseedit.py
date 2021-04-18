# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'exerciseedit.ui'
##
## Created by: Qt User Interface Compiler version 6.0.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ExerciseEdit(object):
    def setupUi(self, ExerciseEdit):
        if not ExerciseEdit.objectName():
            ExerciseEdit.setObjectName(u"ExerciseEdit")
        ExerciseEdit.resize(267, 247)
        self.gridLayout = QGridLayout(ExerciseEdit)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.labelName = QLabel(ExerciseEdit)
        self.labelName.setObjectName(u"labelName")
        self.labelName.setWordWrap(True)

        self.verticalLayout.addWidget(self.labelName)

        self.nameEdit = QLineEdit(ExerciseEdit)
        self.nameEdit.setObjectName(u"nameEdit")

        self.verticalLayout.addWidget(self.nameEdit)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.labelText1 = QLabel(ExerciseEdit)
        self.labelText1.setObjectName(u"labelText1")
        self.labelText1.setWordWrap(True)

        self.verticalLayout.addWidget(self.labelText1)

        self.labelText2 = QLabel(ExerciseEdit)
        self.labelText2.setObjectName(u"labelText2")
        self.labelText2.setWordWrap(True)

        self.verticalLayout.addWidget(self.labelText2)

        self.textEdit = QLineEdit(ExerciseEdit)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout.addWidget(self.textEdit)

        self.labelStatus = QLabel(ExerciseEdit)
        self.labelStatus.setObjectName(u"labelStatus")

        self.verticalLayout.addWidget(self.labelStatus)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.saveButton = QPushButton(ExerciseEdit)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout.addWidget(self.saveButton)

        self.cancelButton = QPushButton(ExerciseEdit)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout.addWidget(self.cancelButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(ExerciseEdit)

        QMetaObject.connectSlotsByName(ExerciseEdit)
    # setupUi

    def retranslateUi(self, ExerciseEdit):
        ExerciseEdit.setWindowTitle(QCoreApplication.translate("ExerciseEdit", u"Edit exercise", None))
        self.labelName.setText(QCoreApplication.translate("ExerciseEdit", u"Choose a name for the exercise", None))
        self.labelText1.setText(QCoreApplication.translate("ExerciseEdit", u"Enter a sequence of notes relative to the base one, expressed as semitone distance, separated by space.", None))
        self.labelText2.setText(QCoreApplication.translate("ExerciseEdit", u"For example: if the selected note is C3 and you wish to play \"D3, D3#, E, C3\" enter \"2 3 4 0\".", None))
        self.labelStatus.setText("")
        self.saveButton.setText(QCoreApplication.translate("ExerciseEdit", u"Save", None))
        self.cancelButton.setText(QCoreApplication.translate("ExerciseEdit", u"Cancel", None))
    # retranslateUi

