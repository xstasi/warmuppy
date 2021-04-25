import os

import pygame
import tempfile

from PySide2.QtCore import QSettings

from mido import Message, MidiFile, MidiTrack

from warmuppy.resources import resources # noqa
from warmuppy.constants import INSTRUMENTS

class Settings():

    def __init__(self, parent=None):

        # Standard constructor stuff
        super().__init__()
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
        self.settings.endArray()

    def remove_exercise(self,exname):
        # Replace self.exercises with a copy without the selected exercise
        new_exercises = []
        for ex in self.exercises:
            if ex[0] != exname:
                new_exercises.append(ex)
        self.exercises = new_exercises

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
