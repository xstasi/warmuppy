# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
##
## Created by: Qt User Interface Compiler version 6.0.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.resize(369, 372)
        self.gridLayout = QGridLayout(Settings)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabWidget = QTabWidget(Settings)
        self.tabWidget.setObjectName(u"tabWidget")
        self.exerciseTab = QWidget()
        self.exerciseTab.setObjectName(u"exerciseTab")
        self.verticalLayout = QVBoxLayout(self.exerciseTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.exerciseList = QListWidget(self.exerciseTab)
        self.exerciseList.setObjectName(u"exerciseList")

        self.verticalLayout.addWidget(self.exerciseList)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.addButton = QPushButton(self.exerciseTab)
        self.addButton.setObjectName(u"addButton")

        self.horizontalLayout.addWidget(self.addButton)

        self.editButton = QPushButton(self.exerciseTab)
        self.editButton.setObjectName(u"editButton")

        self.horizontalLayout.addWidget(self.editButton)

        self.removeButton = QPushButton(self.exerciseTab)
        self.removeButton.setObjectName(u"removeButton")

        self.horizontalLayout.addWidget(self.removeButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.exerciseTab, "")
        self.instrumentsTab = QWidget()
        self.instrumentsTab.setObjectName(u"instrumentsTab")
        self.horizontalLayout_3 = QHBoxLayout(self.instrumentsTab)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.instrumentsTab)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label)

        self.label_2 = QLabel(self.instrumentsTab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.instrumentList = QListWidget(self.instrumentsTab)
        self.instrumentList.setObjectName(u"instrumentList")

        self.horizontalLayout_4.addWidget(self.instrumentList)

        self.previewButton = QPushButton(self.instrumentsTab)
        self.previewButton.setObjectName(u"previewButton")

        self.horizontalLayout_4.addWidget(self.previewButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.tabWidget.addTab(self.instrumentsTab, "")

        self.verticalLayout_2.addWidget(self.tabWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.saveButton = QPushButton(Settings)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout_2.addWidget(self.saveButton)

        self.cancelButton = QPushButton(Settings)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout_2.addWidget(self.cancelButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)


        self.retranslateUi(Settings)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Settings)
    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("Settings", u"Dialog", None))
        self.addButton.setText(QCoreApplication.translate("Settings", u"Add", None))
        self.editButton.setText(QCoreApplication.translate("Settings", u"Edit", None))
        self.removeButton.setText(QCoreApplication.translate("Settings", u"Remove", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.exerciseTab), QCoreApplication.translate("Settings", u"Exercises", None))
#if QT_CONFIG(accessibility)
        self.instrumentsTab.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.label.setText(QCoreApplication.translate("Settings", u"Choose the instrument to use. You can preview the sound using the play button.", None))
        self.label_2.setText(QCoreApplication.translate("Settings", u"Warning: some instruments may be missing, depending on the MIDI library shipped with your operating system.", None))
        self.previewButton.setText(QCoreApplication.translate("Settings", u"Preview", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.instrumentsTab), QCoreApplication.translate("Settings", u"Instruments", None))
        self.saveButton.setText(QCoreApplication.translate("Settings", u"Save", None))
        self.cancelButton.setText(QCoreApplication.translate("Settings", u"Cancel", None))
    # retranslateUi

