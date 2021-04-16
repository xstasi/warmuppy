import os
import logging
from ui.exerciseedit import Ui_ExerciseEdit

from PySide2.QtWidgets import QDialog

from PySide2.QtCore import Signal

from PySide2.QtGui import QIcon

import resources.resources

class exerciseEditWindow(QDialog):

    exercise_signal = Signal(str, str)

    def __init__(self, op, exname='', extext='', exercises=[], parent=None):

        # Standard constructor stuff
        super(exerciseEditWindow, self).__init__()
        self.ui = Ui_ExerciseEdit()
        self.setWindowIcon(QIcon(':/icons/icon.ico'))
        self.ui.setupUi(self)
        if os.getenv("DEBUG") == 'TRUE':
            logging.basicConfig(level=logging.DEBUG)

        # Instance variables
        self.parent = parent
        self.op = op
        self.exname = exname
        self.extext = extext
        self.exercises = exercises

        # Start new exercies as invalid to prevent saving empty stuff
        if op == 'add':
            self.ui.saveButton.setEnabled(False)
        else:
            # Existing exercises are assumed to be already good
            self.ui.labelStatus.setText('OK')

        # Fill exercise edit form with what we got in the constructor
        self.ui.nameEdit.setText(exname)
        self.ui.textEdit.setText(extext)

        # Setup signals
        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.saveButton.clicked.connect(self.save_settings)
        self.ui.nameEdit.textChanged.connect(self.validate)
        self.ui.textEdit.textChanged.connect(self.validate)
        self.exercise_signal.connect(self.send_signal)

    # Signal with exercise name and content to send to parent
    def send_signal(self):
        self.parent.exercise_signal.emit(self.exname, self.extext)

    # 'Save' button handler
    def save_settings(self):
        self.send_signal()
        self.close()

    # Exercise validator
    def validate(self):
        is_junk = False
        self.exname = self.ui.nameEdit.text()
        self.extext = self.ui.textEdit.text()

        # Check that all parts of exercise are numbers
        steps = self.extext.split()
        for step in steps:
            try:
                int(step)
            except ValueError:
                is_junk = True

        # Assume that exercise data is invalid
        self.ui.saveButton.setEnabled(False)

        if self.exname == '':
            self.ui.labelStatus.setText('Missing exercise name')
            return
        if self.extext == '':
            self.ui.labelStatus.setText('Missing exercise data')
            return
        if is_junk:
            self.ui.labelStatus.setText('Invalid exercise data')
            return

        # Do not allow two exercises with the same name
        if self.op == 'add' and self.exname in self.exercises:
            self.ui.labelStatus.setText('Duplicate exercise name')
            return

        logging.debug(f"Name: {self.exname}")
        logging.debug(f"Text: {self.extext}")
        self.ui.labelStatus.setText('OK')
        self.ui.saveButton.setEnabled(True)
