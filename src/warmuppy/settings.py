import os

import pygame
import tempfile

from PySide2.QtWidgets import QStyle, QDialog
from PySide2.QtCore import QSettings, Signal
from PySide2.QtGui import QIcon

from mido import Message, MidiFile, MidiTrack

from warmuppy.ui.settings import Ui_Settings
from warmuppy.exerciseedit import exerciseEditWindow
from warmuppy.resources import resources # noqa
from warmuppy.constants import INSTRUMENTS

pygame.init()


class settingswindow(QDialog):

    # Empty signal to tell the main window that settings changed
    settings_signal = Signal()
    # Connected to the exercise editor, to receive name/data from it
    exercise_signal = Signal(str, str)

    def __init__(self, parent=None):

        # Standard constructor stuff
        super(settingswindow, self).__init__()
        self.ui = Ui_Settings()
        if parent:
            self.settings_signal.connect(parent.settings_signal.emit)
        self.setWindowIcon(QIcon(':/icons/icon.ico'))
        self.ui.setupUi(self)
        self.settings = QSettings()

        # Instance variables
        self.exercises = []
        self.instrument = int(self.settings.value('instrument'))

        # Load exercises from stored settings
        self.settings.beginReadArray('exercises')
        for ex in self.settings.allKeys():
            if ex == 'size':
                continue
            self.exercises.append([
                ex,
                self.settings.value(ex)
            ])
            self.ui.exerciseList.addItem(ex)
        self.settings.endArray()

        # Load instruments from the program constants
        for inst in INSTRUMENTS:
            self.ui.instrumentList.addItem(inst)
        self.ui.instrumentList.setCurrentRow(self.instrument)

        # Nothing is selected by default so disable edit and remove
        self.ui.editButton.setEnabled(False)
        self.ui.removeButton.setEnabled(False)

        # Restyle buttons to use QT builtin icons,
        #  which cannot be done on qtdesigner
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
        self.ui.removeButton.clicked.connect(self.remove_exercise)
        self.ui.exerciseList.currentItemChanged.connect(self.exercise_clicked)

        # Sub-dialog signals
        self.exercise_signal.connect(self.reload_exercise)

    def remove_exercise(self):
        # Get selected exercise
        exname = self.ui.exerciseList.currentItem().text()

        # Replace self.exercises with a copy without the selected exercise
        new_exercises = []
        for ex in self.exercises:
            if ex[0] != exname:
                new_exercises.append(ex)
        self.exercises = new_exercises

        # Reload the UI exercise list from memory
        self.ui.exerciseList.clear()
        for ex in self.exercises:
            self.ui.exerciseList.addItem(ex[0])

    def reload_exercise(self, exname, extext):
        # Load all exercise names
        exercise_names = []
        for ex in self.exercises:
            exercise_names.append(ex[0])
        new_exercises = []
        # If the reloaded exercise is existing then update it in memory,
        #   otherwise just add it
        if exname in exercise_names:
            for ex in self.exercises:
                if ex[0] == exname:
                    new_exercises.append(
                        [ex[0], extext.split()]
                    )
                else:
                    new_exercises.append(
                        [ex[0], ex[1]]
                    )
            self.exercises = new_exercises
        else:
            self.exercises.append([exname, extext.split()])

        # Reload UI exercises
        self.ui.exerciseList.clear()
        for ex in self.exercises:
            self.ui.exerciseList.addItem(ex[0])

    def set_instrument(self, s):
        instrument_name = s.text()
        instrument_id = INSTRUMENTS.index(instrument_name)
        self.instrument = instrument_id

    def save_settings(self):
        self.settings.beginWriteArray('exercises')
        for key in self.settings.allKeys():
            self.settings.remove(key) if key != 'size' else None
        for ex in self.exercises:
            self.settings.setValue(ex[0], ex[1])
        self.settings.endArray()
        self.settings.setValue('instrument', self.instrument)
        # Let parent know that settings were changed
        self.settings_signal.emit()
        self.close()

    def preview(self):
        pygame.mixer.music.stop()
        midi_file = tempfile.NamedTemporaryFile(delete=False)
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)
        prog = self.instrument
        track.append(Message('program_change', program=prog, time=0))
        note = 60
        track.append(
            Message('note_on', note=(note), velocity=100, time=0)
        )
        track.append(
            Message('note_off', note=(note), time=2000)
        )
        mid.save(file=midi_file)
        midi_file.flush()
        midi_file.close()
        pygame.mixer.music.load(midi_file.name)
        pygame.mixer.music.play()
        os.remove(midi_file.name)

    def exercise_clicked(self, a):
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
        w = exerciseEditWindow(
            op='add', parent=self, exercises=exercise_names
        )
        w.exec_()

    def edit_exercise(self):
        exname = self.ui.exerciseList.currentItem().text()
        for ex in self.exercises:
            if ex[0] == exname:
                extext = ' '.join(list(map(str, ex[1])))
        w = exerciseEditWindow(
            op='edit', parent=self, exname=exname, extext=extext
        )
        w.exec_()
