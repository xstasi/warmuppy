import logging

from warmuppy.ui.dialogs.exerciseeditwindow import Ui_ExerciseEditWindow

from PySide2.QtWidgets import QDialog

from PySide2.QtCore import Signal

from PySide2.QtGui import QIcon

from warmuppy.resources import resources # noqa


# Generic exercise editing window
class ExerciseEditWindow(QDialog):

    # Used to transmit the exercise name and data back to the settings window
    exercise_signal = Signal(str, str)

    def __init__(self, op, exname='', extext='', exercises=[], parent=None):

        # Standard constructor stuff
        super().__init__()
        self.ui = Ui_ExerciseEditWindow()
        self.setWindowIcon(QIcon(':/icons/icon.ico'))
        self.ui.setupUi(self)

        # Instance variables
        self.parent = parent
        self.op = op
        self.exercise_name = exname
        self.exercise_text = extext
        self.exercises = exercises

        if op == 'add':
            # Start new exercises as invalid to prevent saving empty stuff
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
        self.parent.exercise_signal.emit(self.exercise_name, self.exercise_text)

    # 'Save' button handler
    def save_settings(self):
        self.send_signal()
        self.close()

    # Exercise validator
    def validate(self):
        is_junk = False
        self.exercise_name = self.ui.nameEdit.text()
        self.exercise_text = self.ui.textEdit.text()

        # Check that all parts of exercise are numbers
        steps = self.exercise_text.split()
        for step in steps:
            try:
                int(step)
            except ValueError:
                is_junk = True

        # Assume that exercise data is invalid
        self.ui.saveButton.setEnabled(False)

        if self.exercise_name == '':
            self.ui.labelStatus.setText('Missing exercise name')
            return
        if self.exercise_text == '':
            self.ui.labelStatus.setText('Missing exercise data')
            return
        if is_junk:
            self.ui.labelStatus.setText('Invalid exercise data')
            return

        # Do not allow two exercises with the same name
        if self.op == 'add' and self.exercise_name in self.exercises:
            self.ui.labelStatus.setText('Duplicate exercise name')
            return

        logging.debug(f"Name: {self.exercise_name}")
        logging.debug(f"Text: {self.exercise_text}")
        self.ui.labelStatus.setText('OK')
        self.ui.saveButton.setEnabled(True)
