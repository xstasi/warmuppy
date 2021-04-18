# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.0.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(601, 282)
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionHow_to_use = QAction(MainWindow)
        self.actionHow_to_use.setObjectName(u"actionHow_to_use")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.verticalLayout.addWidget(self.progressBar)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.horizontalLayout_8 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_13)

        self.labelNote = QLabel(self.layoutWidget)
        self.labelNote.setObjectName(u"labelNote")

        self.horizontalLayout_8.addWidget(self.labelNote)

        self.radioButton_C = QRadioButton(self.layoutWidget)
        self.radioButton_C.setObjectName(u"radioButton_C")

        self.horizontalLayout_8.addWidget(self.radioButton_C)

        self.radioButton_Cs = QRadioButton(self.layoutWidget)
        self.radioButton_Cs.setObjectName(u"radioButton_Cs")
        self.radioButton_Cs.setChecked(True)

        self.horizontalLayout_8.addWidget(self.radioButton_Cs)

        self.radioButton_D = QRadioButton(self.layoutWidget)
        self.radioButton_D.setObjectName(u"radioButton_D")

        self.horizontalLayout_8.addWidget(self.radioButton_D)

        self.radioButton_Ds = QRadioButton(self.layoutWidget)
        self.radioButton_Ds.setObjectName(u"radioButton_Ds")

        self.horizontalLayout_8.addWidget(self.radioButton_Ds)

        self.radioButton_E = QRadioButton(self.layoutWidget)
        self.radioButton_E.setObjectName(u"radioButton_E")

        self.horizontalLayout_8.addWidget(self.radioButton_E)

        self.radioButton_F = QRadioButton(self.layoutWidget)
        self.radioButton_F.setObjectName(u"radioButton_F")

        self.horizontalLayout_8.addWidget(self.radioButton_F)

        self.radioButton_Fs = QRadioButton(self.layoutWidget)
        self.radioButton_Fs.setObjectName(u"radioButton_Fs")

        self.horizontalLayout_8.addWidget(self.radioButton_Fs)

        self.radioButton_G = QRadioButton(self.layoutWidget)
        self.radioButton_G.setObjectName(u"radioButton_G")

        self.horizontalLayout_8.addWidget(self.radioButton_G)

        self.radioButton_Gs = QRadioButton(self.layoutWidget)
        self.radioButton_Gs.setObjectName(u"radioButton_Gs")

        self.horizontalLayout_8.addWidget(self.radioButton_Gs)

        self.radioButton_A = QRadioButton(self.layoutWidget)
        self.radioButton_A.setObjectName(u"radioButton_A")

        self.horizontalLayout_8.addWidget(self.radioButton_A)

        self.radioButton_As = QRadioButton(self.layoutWidget)
        self.radioButton_As.setObjectName(u"radioButton_As")

        self.horizontalLayout_8.addWidget(self.radioButton_As)

        self.radioButton_B = QRadioButton(self.layoutWidget)
        self.radioButton_B.setObjectName(u"radioButton_B")

        self.horizontalLayout_8.addWidget(self.radioButton_B)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_14)

        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget1 = QWidget(self.splitter)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.horizontalLayout_9 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_5)

        self.labelOctave = QLabel(self.layoutWidget1)
        self.labelOctave.setObjectName(u"labelOctave")

        self.horizontalLayout_9.addWidget(self.labelOctave)

        self.radioButton_O1 = QRadioButton(self.layoutWidget1)
        self.radioButton_O1.setObjectName(u"radioButton_O1")

        self.horizontalLayout_9.addWidget(self.radioButton_O1)

        self.radioButton_O2 = QRadioButton(self.layoutWidget1)
        self.radioButton_O2.setObjectName(u"radioButton_O2")

        self.horizontalLayout_9.addWidget(self.radioButton_O2)

        self.radioButton_O3 = QRadioButton(self.layoutWidget1)
        self.radioButton_O3.setObjectName(u"radioButton_O3")

        self.horizontalLayout_9.addWidget(self.radioButton_O3)

        self.radioButton_O4 = QRadioButton(self.layoutWidget1)
        self.radioButton_O4.setObjectName(u"radioButton_O4")

        self.horizontalLayout_9.addWidget(self.radioButton_O4)

        self.radioButton_O5 = QRadioButton(self.layoutWidget1)
        self.radioButton_O5.setObjectName(u"radioButton_O5")

        self.horizontalLayout_9.addWidget(self.radioButton_O5)

        self.radioButton_O6 = QRadioButton(self.layoutWidget1)
        self.radioButton_O6.setObjectName(u"radioButton_O6")

        self.horizontalLayout_9.addWidget(self.radioButton_O6)

        self.radioButton_O7 = QRadioButton(self.layoutWidget1)
        self.radioButton_O7.setObjectName(u"radioButton_O7")

        self.horizontalLayout_9.addWidget(self.radioButton_O7)

        self.radioButton_O8 = QRadioButton(self.layoutWidget1)
        self.radioButton_O8.setObjectName(u"radioButton_O8")

        self.horizontalLayout_9.addWidget(self.radioButton_O8)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_6)

        self.splitter.addWidget(self.layoutWidget1)

        self.verticalLayout.addWidget(self.splitter)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.labelStep = QLabel(self.centralwidget)
        self.labelStep.setObjectName(u"labelStep")

        self.horizontalLayout_2.addWidget(self.labelStep)

        self.spinStep = QSpinBox(self.centralwidget)
        self.spinStep.setObjectName(u"spinStep")
        self.spinStep.setMinimum(1)
        self.spinStep.setMaximum(12)

        self.horizontalLayout_2.addWidget(self.spinStep)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.labelBPM = QLabel(self.centralwidget)
        self.labelBPM.setObjectName(u"labelBPM")

        self.horizontalLayout_2.addWidget(self.labelBPM)

        self.spinBPM = QSpinBox(self.centralwidget)
        self.spinBPM.setObjectName(u"spinBPM")
        self.spinBPM.setMaximum(200)
        self.spinBPM.setValue(100)

        self.horizontalLayout_2.addWidget(self.spinBPM)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_7)

        self.labelCut = QLabel(self.centralwidget)
        self.labelCut.setObjectName(u"labelCut")

        self.horizontalLayout_2.addWidget(self.labelCut)

        self.spinCut = QDoubleSpinBox(self.centralwidget)
        self.spinCut.setObjectName(u"spinCut")
        self.spinCut.setDecimals(3)
        self.spinCut.setMaximum(1.000000000000000)
        self.spinCut.setSingleStep(0.005000000000000)
        self.spinCut.setValue(0.020000000000000)

        self.horizontalLayout_2.addWidget(self.spinCut)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_8)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_10)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.previewCheckBox = QCheckBox(self.centralwidget)
        self.previewCheckBox.setObjectName(u"previewCheckBox")
        self.previewCheckBox.setChecked(True)

        self.verticalLayout_2.addWidget(self.previewCheckBox)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.labelPreview = QLabel(self.centralwidget)
        self.labelPreview.setObjectName(u"labelPreview")

        self.horizontalLayout_4.addWidget(self.labelPreview)

        self.spinPreview = QSpinBox(self.centralwidget)
        self.spinPreview.setObjectName(u"spinPreview")

        self.horizontalLayout_4.addWidget(self.spinPreview)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_12)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.prolongCheckBox = QCheckBox(self.centralwidget)
        self.prolongCheckBox.setObjectName(u"prolongCheckBox")

        self.verticalLayout_3.addWidget(self.prolongCheckBox)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.labelProlong = QLabel(self.centralwidget)
        self.labelProlong.setObjectName(u"labelProlong")

        self.horizontalLayout_5.addWidget(self.labelProlong)

        self.spinProlong = QSpinBox(self.centralwidget)
        self.spinProlong.setObjectName(u"spinProlong")

        self.horizontalLayout_5.addWidget(self.spinProlong)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_11)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.labelExercise = QLabel(self.centralwidget)
        self.labelExercise.setObjectName(u"labelExercise")

        self.horizontalLayout.addWidget(self.labelExercise)

        self.comboExercise = QComboBox(self.centralwidget)
        self.comboExercise.setObjectName(u"comboExercise")

        self.horizontalLayout.addWidget(self.comboExercise)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_9)

        self.lowerButton = QPushButton(self.centralwidget)
        self.lowerButton.setObjectName(u"lowerButton")

        self.horizontalLayout.addWidget(self.lowerButton)

        self.playButton = QPushButton(self.centralwidget)
        self.playButton.setObjectName(u"playButton")

        self.horizontalLayout.addWidget(self.playButton)

        self.stopButton = QPushButton(self.centralwidget)
        self.stopButton.setObjectName(u"stopButton")

        self.horizontalLayout.addWidget(self.stopButton)

        self.higherButton = QPushButton(self.centralwidget)
        self.higherButton.setObjectName(u"higherButton")

        self.horizontalLayout.addWidget(self.higherButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 601, 20))
        self.menuMain = QMenu(self.menubar)
        self.menuMain.setObjectName(u"menuMain")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuMain.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuMain.addSeparator()
        self.menuMain.addAction(self.actionSettings)
        self.menuMain.addSeparator()
        self.menuMain.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionHow_to_use)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Warmuppy", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About Warmuppy", None))
        self.actionHow_to_use.setText(QCoreApplication.translate("MainWindow", u"How to use", None))
        self.labelNote.setText(QCoreApplication.translate("MainWindow", u"Note: ", None))
        self.radioButton_C.setText(QCoreApplication.translate("MainWindow", u"C", None))
        self.radioButton_Cs.setText(QCoreApplication.translate("MainWindow", u"C#", None))
        self.radioButton_D.setText(QCoreApplication.translate("MainWindow", u"D", None))
        self.radioButton_Ds.setText(QCoreApplication.translate("MainWindow", u"D#", None))
        self.radioButton_E.setText(QCoreApplication.translate("MainWindow", u"E", None))
        self.radioButton_F.setText(QCoreApplication.translate("MainWindow", u"F", None))
        self.radioButton_Fs.setText(QCoreApplication.translate("MainWindow", u"F#", None))
        self.radioButton_G.setText(QCoreApplication.translate("MainWindow", u"G", None))
        self.radioButton_Gs.setText(QCoreApplication.translate("MainWindow", u"G#", None))
        self.radioButton_A.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.radioButton_As.setText(QCoreApplication.translate("MainWindow", u"A#", None))
        self.radioButton_B.setText(QCoreApplication.translate("MainWindow", u"B", None))
        self.labelOctave.setText(QCoreApplication.translate("MainWindow", u"Octave:", None))
        self.radioButton_O1.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.radioButton_O2.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.radioButton_O3.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.radioButton_O4.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.radioButton_O5.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.radioButton_O6.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.radioButton_O7.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.radioButton_O8.setText(QCoreApplication.translate("MainWindow", u"8", None))
        self.labelStep.setText(QCoreApplication.translate("MainWindow", u"Step", None))
        self.labelBPM.setText(QCoreApplication.translate("MainWindow", u"BPM", None))
        self.labelCut.setText(QCoreApplication.translate("MainWindow", u"Cut", None))
        self.previewCheckBox.setText(QCoreApplication.translate("MainWindow", u"Preview base note", None))
        self.labelPreview.setText(QCoreApplication.translate("MainWindow", u"Preview duration (beats)", None))
        self.prolongCheckBox.setText(QCoreApplication.translate("MainWindow", u"Prolong trailing note", None))
        self.labelProlong.setText(QCoreApplication.translate("MainWindow", u"Prolonged length (beats)", None))
        self.labelExercise.setText(QCoreApplication.translate("MainWindow", u"Exercise", None))
        self.lowerButton.setText(QCoreApplication.translate("MainWindow", u"Lower", None))
        self.playButton.setText(QCoreApplication.translate("MainWindow", u"Play", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.higherButton.setText(QCoreApplication.translate("MainWindow", u"Higher", None))
        self.menuMain.setTitle(QCoreApplication.translate("MainWindow", u"Warmuppy", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

