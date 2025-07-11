import os

import tempfile

from PySide6.QtCore import QSettings

from mido import Message, MidiFile, MidiTrack

from warmuppy.resources import resources  # noqa
from warmuppy.warmuppy_player import WarmuppyPlayer

from shutil import copyfile


class Settings:

    def __init__(self):

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
        self.player = WarmuppyPlayer()

    def remove_exercise(self, exercise_name):
        # Replace self.exercises with a copy without the selected exercise
        new_exercises = []
        for ex in self.exercises:
            if ex[0] != exercise_name:
                new_exercises.append(ex)
        self.exercises = new_exercises

    def reload_exercise(self, exercise_name, exercise_text):
        # Load all exercise names
        exercise_names = []
        for ex in self.exercises:
            exercise_names.append(ex[0])
        new_exercises = []
        # If the reloaded exercise is existing then update it in memory,
        #   otherwise just add it
        exercise_contents = exercise_text.split()
        if exercise_name in exercise_names:
            for ex in self.exercises:
                if ex[0] == exercise_name:
                    new_exercises.append(
                        [ex[0], exercise_contents]
                    )
                else:
                    new_exercises.append(
                        [ex[0], ex[1]]
                    )
            self.exercises = new_exercises
        else:
            self.exercises.append([exercise_name, exercise_contents])

    def set_instrument(self, instrument_id):
        self.instrument = instrument_id

    def save_settings(self):
        self.settings.beginWriteArray('exercises')
        for key in self.settings.allKeys():
            self.settings.remove(key) if key != 'size' else None
        for ex in self.exercises:
            self.settings.setValue(ex[0], ex[1])
        self.settings.endArray()
        self.settings.setValue('instrument', self.instrument)
        self.settings.sync()

    def preview(self):
        midi_file = tempfile.NamedTemporaryFile(delete=False)
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)
        instrument = self.instrument
        track.append(Message('program_change', program=instrument, time=0))
        note = 60
        track.append(
            Message('note_on', note=note, velocity=100, time=0)
        )
        track.append(
            Message('note_off', note=note, time=2000)
        )
        mid.save(file=midi_file)
        midi_file.flush()
        midi_file.close()
        self.player.play(midi_file.name)

        if 'WARMUPPY_KEEP_MIDI' in os.environ:
            copyfile(midi_file.name, os.environ['WARMUPPY_KEEP_MIDI'])
        os.remove(midi_file.name)
