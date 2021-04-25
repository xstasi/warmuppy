import logging

from PySide2.QtWidgets import (
    QMainWindow, QRadioButton, QStyle
)
from PySide2.QtCore import QTimer
from PySide2.QtGui import QIcon

from warmuppy.ui.dialogs.warmuppywindow import Ui_WarmuppyWindow

from warmuppy.ui.settings_window import SettingsWindow
from warmuppy.ui.about_window import AboutWindow
from warmuppy.ui.howto_window import HowtoWindow

from warmuppy.resources import resources # noqa
from warmuppy.constants import NOTES
from warmuppy.warmuppy import Warmuppy


class WarmuppyWindow(Warmuppy, QMainWindow):

    def __init__(self):
        super().__init__()

        # Load UI
        self.ui = Ui_WarmuppyWindow()
        self.setWindowIcon(QIcon(':/icons/icon.ico'))
        self.ui.setupUi(self)

        # Restyle buttons to use QT builtin icons,
        #  which cannot be done on qt designer
        self.ui.playButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay)
        )
        self.ui.stopButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaStop)
        )
        self.ui.lowerButton.setIcon(
            self.style().standardIcon(QStyle.SP_ArrowDown)
        )
        self.ui.higherButton.setIcon(
            self.style().standardIcon(QStyle.SP_ArrowUp)
        )

        # Setup signals
        self.ui.comboExercise.currentIndexChanged.connect(self.change_exercise)
        self.ui.higherButton.clicked.connect(lambda: self.bump_note(True))
        self.ui.lowerButton.clicked.connect(lambda: self.bump_note(False))
        self.ui.playButton.clicked.connect(self.play_exercise)
        self.ui.stopButton.clicked.connect(self.stop)
        self.ui.spinBPM.valueChanged.connect(self.change_bpm)
        self.ui.spinCut.valueChanged.connect(self.change_cut)
        self.ui.spinStep.valueChanged.connect(self.change_step)
        self.ui.previewCheckBox.toggled.connect(self.change_preview)
        self.ui.spinPreview.valueChanged.connect(self.change_preview_time)
        self.ui.spinProlong.valueChanged.connect(self.change_prolong_time)
        self.ui.prolongCheckBox.toggled.connect(self.change_prolong)
        # Menus
        self.ui.actionSettings.triggered.connect(self.show_settings)
        self.ui.actionAbout.triggered.connect(self.show_about)
        self.ui.actionHow_to_use.triggered.connect(self.show_howto)
        self.ui.actionExit.triggered.connect(self.close)
        # Note/octave radio buttons
        for note in NOTES:
            x = self.findChild(QRadioButton, f"radioButton_{note}")
            x.toggled.connect(
                lambda toggled, note=note:
                    self.change_note(note) if toggled else None
            )
        for octave in range(1, 8):
            x = self.findChild(QRadioButton, f"radioButton_O{octave}")
            x.toggled.connect(
                lambda toggled, octave=octave:
                    self.change_octave(octave) if toggled else None
            )

        # Load UI data
        for ex in self.exercises:
            self.ui.comboExercise.addItem(ex[0])
        ex_text = self.exercises[self.exercise][0]
        self.ui.comboExercise.setCurrentText(ex_text)
        self.ui.progressBar.setValue(0)
        cur_note = self.notes[self.note]
        self.findChild(
            QRadioButton, f"radioButton_{cur_note}"
        ).setChecked(True)
        self.findChild(
            QRadioButton, f"radioButton_O{self.octave}"
        ).setChecked(True)
        self.ui.previewCheckBox.setChecked(self.preview)
        self.ui.prolongCheckBox.setChecked(self.prolong)
        self.ui.spinBPM.setValue(self.bpm)
        self.ui.spinCut.setValue(self.cut)
        self.ui.spinStep.setValue(self.step)
        self.ui.spinProlong.setValue(self.prolong_time)
        self.ui.spinPreview.setValue(self.preview_time)

    def show_about(self):
        w = AboutWindow()
        w.exec_()

    def show_settings(self):
        w = SettingsWindow()
        w.settings_signal.connect(self.reload_settings)
        w.exec_()

    def show_howto(self):
        w = HowtoWindow()
        w.exec_()

    def change_preview(self, p):
        super().change_preview(p)
        self.ui.spinPreview.setEnabled(p)

    def change_prolong(self, p):
        super().change_prolong(p)
        self.ui.spinProlong.setEnabled(p)

    # Go {step} semitones up or down
    def bump_note(self, up):
        octave, note = super().bump_note(up)

        octave_radio = self.findChild(QRadioButton, f"radioButton_O{octave}")
        octave_radio.setChecked(True)

        note_radio = self.findChild(QRadioButton, f"radioButton_{note}")
        note_radio.setChecked(True)

        self.play_exercise()

    # Generate a midi with the exercise and then play it
    def play_exercise(self):

        self.ui.progressBar.setValue(0)

        timer_data = super().play_exercise()

        logging.debug(timer_data)
        for percent, delay in timer_data:

            # Create a new timer for the progress bar
            self.timers.append(QTimer())
            timer = self.timers[-1]
            timer.setSingleShot(True)
            timer.timeout.connect(
                lambda pc=percent: self.ui.progressBar.setValue(pc)
            )

            logging.debug(f"Setting timer for {percent}% after {delay}ms")
            timer.setInterval(delay)

        # Once midi is loaded, start the % timers and play it
        for timer in self.timers:
            timer.start()

    def stop(self):
        super().stop()
        for timer in self.timers:
            timer.stop()
        self.timers = []
        # Reset progress
        self.ui.progressBar.setValue(0)

    # Settings window told us that something changed, so reload everything
    def reload_settings(self):
        super().reload_settings()
        self.ui.comboExercise.clear()
        for ex, v in self.exercises:
            self.ui.comboExercise.addItem(ex)
