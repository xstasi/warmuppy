import logging

from PySide6.QtWidgets import QStyle, QDialog
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon

from warmuppy.ui.dialogs.settingswindow import Ui_SettingsWindow
from warmuppy.ui.exercise_edit_window import ExerciseEditWindow

from warmuppy.settings import Settings
from warmuppy.resources import resources # noqa
from warmuppy.constants import INSTRUMENTS


class SettingsWindow(Settings, QDialog):

    # Empty signal to tell the main window that settings changed
    settings_signal = Signal()
    # Connected to the exercise editor, to receive name/data from it
    exercise_signal = Signal(str, str)

    def __init__(self):

        # Standard constructor stuff
        super().__init__()
        self.ui = Ui_SettingsWindow()
        self.setWindowIcon(QIcon(':/icons/icon.ico'))
        self.ui.setupUi(self)

        # Load exercises from stored settings
        for ex, v in self.exercises:
            if ex == 'size':
                continue
            self.ui.exerciseList.addItem(ex)

        # Load instruments from the program constants
        for inst in INSTRUMENTS:
            self.ui.instrumentList.addItem(inst)
        self.ui.instrumentList.setCurrentRow(self.instrument)

        # Nothing is selected by default so disable edit and remove
        self.ui.editButton.setEnabled(False)
        self.ui.removeButton.setEnabled(False)

        # Restyle buttons to use QT builtin icons,
        #  which cannot be done on qt designer
        self.ui.previewButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay)
        )

        # Setup signals
        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.saveButton.clicked.connect(self.save_settings)
        self.ui.previewButton.clicked.connect(self.preview)
        self.ui.instrumentList.currentItemChanged.connect(self.set_instrument)
        self.ui.addButton.clicked.connect(self.add_exercise)
        self.ui.editButton.clicked.connect(self.edit_exercise)
        self.ui.removeButton.clicked.connect(self.remove_exercise_ui)
        self.ui.exerciseList.currentItemChanged.connect(self.exercise_clicked)

        # Sub-dialog signals
        self.exercise_signal.connect(self.reload_exercise)

    def remove_exercise_ui(self):
        # Get selected exercise
        exercise_name = self.ui.exerciseList.currentItem().text()
        super().remove_exercise(exercise_name)

        # Reload the UI exercise list from memory
        self.ui.exerciseList.clear()
        for ex in self.exercises:
            self.ui.exerciseList.addItem(ex[0])

    def reload_exercise(self, exercise_name, exercise_text):

        super().reload_exercise(exercise_name, exercise_text)

        # Reload UI exercises
        self.ui.exerciseList.clear()
        for ex in self.exercises:
            self.ui.exerciseList.addItem(ex[0])

    def save_settings(self):
        super().save_settings()

        # Let parent know that settings were changed
        if self.settings_signal.emit():
            logging.debug("Signal emitted")
        self.close()

    def exercise_clicked(self, _):
        # Enable 'edit' and 'remove' if an exercise was selected
        if self.ui.exerciseList.currentItem():
            self.ui.editButton.setEnabled(True)
            self.ui.removeButton.setEnabled(True)
        else:
            self.ui.editButton.setEnabled(False)
            self.ui.removeButton.setEnabled(False)

    def add_exercise(self):
        exercise_names = []
        for ex in self.exercises:
            exercise_names.append(ex[0])
        w = ExerciseEditWindow(
            op='add', parent=self, exercises=exercise_names
        )
        w.exec_()

    def edit_exercise(self):
        exercise_name = self.ui.exerciseList.currentItem().text()
        exercise_text = ''
        for ex in self.exercises:
            if ex[0] == exercise_name:
                exv=ex[1]
                if isinstance(exv,str):
                    exv=[exv]
                exercise_text = ' '.join(exv)
        w = ExerciseEditWindow(
            op='edit', parent=self, exname=exercise_name, extext=exercise_text
        )
        w.exec_()

    def set_instrument(self, s):
        instrument_name = s.text()
        instrument_id = INSTRUMENTS.index(instrument_name)
        super().set_instrument(instrument_id)
