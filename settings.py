import sys
import os

import pygame
import tempfile
import logging

from ui.settings import Ui_Settings
from exerciseedit import exerciseEditWindow

from PySide2.QtWidgets import (
    QApplication, QStyle, QDialog
)
from PySide2.QtCore import QSettings, QCoreApplication, Signal

from mido import Message, MidiFile, MidiTrack

pygame.init()

APPLICATION_NAME = 'Warmuppy'

INSTRUMENTS = [
    "Acoustic Grand Piano",
    "Bright Acoustic Piano",
    "Electric Grand Piano",
    "Honky-Tonk Piano",
    "Rhodes Piano",
    "Chorused Piano",
    "Harpsichord",
    "Clavinet",
    "Celesta",
    "Glockenspiel",
    "Music Box",
    "Vibraphone",
    "Marimba",
    "Xylophone",
    "Tubular Bells",
    "Dulcimer",
    "Hammond Organ",
    "Percussive Organ",
    "Rock Organ",
    "Church Organ",
    "Reed Organ",
    "Accordion",
    "Harmonica",
    "Tango Accordion",
    "Acoustic Guitar - Nylon",
    "Acoustic Guitar - Steel",
    "Electric Guitar - Jazz",
    "Electric Guitar - Clean",
    "Electric Guitar - Muted",
    "Overdriven Guitar",
    "Distortion Guitar",
    "Guitar Harmonics",
    "Acoustic Bass",
    "Electric Bass - Finger",
    "Electric Bass - Pick",
    "Fretless Bass",
    "Slap Bass 1",
    "Slap Bass 2",
    "Synth Bass 1",
    "Synth Bass 2",
    "Violin",
    "Viola",
    "Cello",
    "Contrabass",
    "Tremolo Strings",
    "Pizzicato Strings",
    "Orchestral Harp",
    "Timpani",
    "String Ensemble 1",
    "String Ensemble 2",
    "Synth. Strings 1",
    "Synth. Strings 2",
    "Choir Aahs",
    "Voice Oohs",
    "Synth Voice",
    "Orchestra Hit",
    "Trumpet",
    "Trombone",
    "Tuba",
    "Muted Trumpet",
    "French Horn",
    "Brass Section",
    "Synth. Brass 1",
    "Synth. Brass 2",
    "Soprano Sax",
    "Alto Sax",
    "Tenor Sax",
    "Baritone Sax",
    "Oboe",
    "English Horn",
    "Bassoon",
    "Clarinet",
    "Piccolo",
    "Flute",
    "Recorder",
    "Pan Flute",
    "Bottle Blow",
    "Shakuhachi",
    "Whistle",
    "Ocarina",
    "Synth Lead 1 - Square",
    "Synth Lead 2 - Sawtooth",
    "Synth Lead 3 - Calliope",
    "Synth Lead 4 - Chiff",
    "Synth Lead 5 - Charang",
    "Synth Lead 6 - Voice",
    "Synth Lead 7 - Fifths",
    "Synth Lead 8 - Brass + Lead",
    "Synth Pad 1 - New Age",
    "Synth Pad 2 - Warm",
    "Synth Pad 3 - Polysynth",
    "Synth Pad 4 - Choir",
    "Synth Pad 5 - Bowed",
    "Synth Pad 6 - Metallic",
    "Synth Pad 7 - Halo",
    "Synth Pad 8 - Sweep"
]

if os.getenv("DEBUG") == 'TRUE':
    logging.basicConfig(level=logging.DEBUG)


class settingswindow(QDialog):

    settings_signal = Signal()
    exercise_signal = Signal(str, str)

    def __init__(self, parent=None):
        super(settingswindow, self).__init__()
        self.ui = Ui_Settings()
        if parent:
            self.settings_signal.connect(parent.settings_signal.emit)
        self.ui.setupUi(self)
        self.settings = QSettings()
        self.exercises = []
        self.instrument = int(self.settings.value('instrument'))
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
        for inst in INSTRUMENTS:
            self.ui.instrumentList.addItem(inst)
        self.ui.instrumentList.setCurrentRow(self.instrument)

        self.ui.editButton.setEnabled(False)

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
        self.ui.exerciseList.currentItemChanged.connect(self.exercise_clicked)

        # Sub-dialog signals
        self.exercise_signal.connect(self.reload_exercise)

    def reload_exercise(self, exname, extext):
        exercise_names = []
        for ex in self.exercises:
            exercise_names.append(ex[0])
        new_exercises = []
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

        self.ui.exerciseList.clear()
        for ex in self.exercises:
            self.ui.exerciseList.addItem(ex[0])
        print(self.exercises)

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
        if self.ui.exerciseList.currentItem():
            self.ui.editButton.setEnabled(True)
        else:
            self.ui.editButton.setEnabled(False)

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


if __name__ == "__main__":
    app = QApplication([])
    QCoreApplication.setOrganizationName(APPLICATION_NAME)
    QCoreApplication.setApplicationName(APPLICATION_NAME)
    widget = settingswindow()
    widget.show()
    sys.exit(app.exec_())
