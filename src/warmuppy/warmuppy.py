import pygame
import tempfile
import logging
import os

from mido import Message, MidiFile, MidiTrack

from PySide2.QtCore import QSettings

from warmuppy.resources import resources # noqa
from warmuppy.constants import (
    NOTES, DEFAULT_INSTRUMENT, DEFAULT_EXERCISE, DEFAULT_EXERCISES,
    DEFAULT_BPM, DEFAULT_CUT, DEFAULT_STEP, DEFAULT_PROLONG, DEFAULT_PREVIEW,
    DEFAULT_PREVIEW_TIME, DEFAULT_PROLONG_TIME,
)


class Warmuppy:

    def __init__(self):

        super().__init__()

        # Instance variables
        self.settings = QSettings()
        self.timers = []
        self.exercises = []
        self.notes = NOTES

        # Load settings
        self.bpm = int(self.settings.value('bpm', DEFAULT_BPM))
        self.cut = float(self.settings.value('cut', DEFAULT_CUT))
        self.step = int(self.settings.value('step', DEFAULT_STEP))
        prev = self.settings.value('preview', DEFAULT_PREVIEW)
        self.preview = prev in ['true', True]
        prolonged = self.settings.value('prolong', DEFAULT_PROLONG)
        self.prolong = prolonged in ['true', True]
        self.preview_time = int(
            self.settings.value('preview_time', DEFAULT_PREVIEW_TIME)
        )
        self.prolong_time = int(
            self.settings.value('prolong_time', DEFAULT_PROLONG_TIME)
        )
        self.note = int(self.settings.value('note', 0))
        self.octave = int(self.settings.value('octave', 3))
        self.instrument = int(
            self.settings.value('instrument', DEFAULT_INSTRUMENT)
        )

        self.settings.beginReadArray('exercises')
        for ex in self.settings.allKeys():
            if ex == 'size':
                continue
            self.exercises.append([
                ex,
                self.settings.value(ex)
            ])
        self.settings.endArray()
        if not self.exercises:
            self.settings.beginWriteArray('exercises')
            for ex in DEFAULT_EXERCISES:
                self.exercises.append(ex)
                self.settings.setValue(ex[0], ex[1])
            self.settings.endArray()
        self.exercise = DEFAULT_EXERCISE
        self.settings.setValue('instrument', self.instrument)

    def change_note(self, note):
        note_id = self.notes.index(note)
        logging.debug(f"New note is {note} ({note_id})")
        self.note = note_id
        self.settings.setValue('note', note_id)

    def change_octave(self, octave):
        logging.debug(f"New octave is {octave}")
        self.octave = octave
        self.settings.setValue('octave', octave)

    def change_exercise(self, i):
        self.exercise = i
        if not self.exercises:
            logging.debug("No exercise to change to, skipping")
            return
        try:
            ex = self.exercises[i]
        except IndexError:
            ex = self.exercises[0]
        logging.debug(f"Selected exercise {ex[0]} ({ex[1]})")

    # Generate boilerplate setters
    for x in "bpm cut step preview_time prolong_time".split():
        exec(f'''def change_{x}(self,{x}):
                    logging.debug("New {x} : %s",{x})
                    self.settings.setValue('{x}',{x})
                    self.{x} = {x}''')

    def change_preview(self, p):
        logging.debug(f"Setting preview as {p}")
        self.preview = p
        self.settings.setValue('preview', p)

    def change_prolong(self, p):
        logging.debug(f"Setting prolong as {p}")
        self.prolong = p
        self.settings.setValue('prolong', p)

    # Go {step} semitones up or down
    def bump_note(self, up):

        self.stop()

        # Beginning of 3rd octave + selected octave * semitones + note
        base_note = 24 + (self.octave - 1) * 12 + self.note
        logging.debug(f"Current note: {base_note}")
        # Highest playable note is the last of the 8th octave
        max_note = 8 * 12 + 24
        # Lowest is C3
        min_note = 25

        # Compute new note
        if up:
            if base_note < max_note:
                base_note += self.step
        else:
            if base_note > min_note:
                base_note -= self.step
        logging.debug(f"New note: {base_note}")

        # Compute new octave
        octave = (base_note - 24) // 12 + 1
        logging.debug(f"New octave should be #{octave}")

        # Compute relative note for the UI
        note_id = (base_note - 24) % 12
        note = self.notes[note_id]
        logging.debug(f"New note should be #{note}")

        return octave, note

    # Generate a midi with the exercise and then play it
    def play_exercise(self):
        self.stop()

        # Load selected exercise
        ex = self.exercises[self.exercise]
        name = ex[0]
        seq = ex[1]
        logging.debug(f"Starting exercise '{name}' (pattern: {seq})")

        # Init midi file
        midi_file = tempfile.NamedTemporaryFile(delete=False)
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)
        track.append(
            Message('program_change', program=self.instrument, time=0)
        )

        # Compute starting note: octave * semitones + relative note
        base_note = 24 + (self.octave - 1) * 12 + self.note
        # Seconds per beat
        seconds = 60 / self.bpm
        # Note duration is one beat minus the cut, in milliseconds
        duration = (seconds - self.cut) * 1000

        # Prepend the base note to the midi if the preview is selected
        timer_delay = 0
        if self.preview:
            timer_delay = int(duration*self.preview_time)
            track.append(
                Message('note_on', note=base_note, velocity=100, time=0)
            )
            track.append(
                Message('note_off', note=base_note, time=timer_delay)
            )

        timer_data = []
        # Add the rest of the notes
        for idx, p in enumerate(seq):

            # Exercises are stored as strings
            step = int(p)

            # Calculate percentage of current step
            current_index = idx + 1
            percent = (current_index / len(seq)) * 100

            # If this is the last note and the user wants to, prolong it
            if current_index == len(seq) and self.prolong:
                logging.debug(f"prolonging {step}")
                delay = int(duration*self.prolong_time)
            else:
                delay = int(duration)

            # Append the note to the midi
            track.append(
                Message('note_on', note=(base_note+step), velocity=100, time=0)
            )
            track.append(
                Message('note_off', note=(base_note+step), time=delay)
            )
            timer_data.append([percent, timer_delay+duration*idx])

        # Save midi file and load it with pygame separately,
        #   to avoid race conditions
        mid.save(file=midi_file)
        midi_file.flush()
        midi_file.close()
        pygame.mixer.music.load(midi_file.name)

        pygame.mixer.music.play()

        # Cleanup
        os.remove(midi_file.name)

        return timer_data

    def stop(self):
        # Stop the music
        pygame.mixer.music.stop()

    # Settings window told us that something changed, so reload everything
    def reload_settings(self):
        logging.debug("Settings saved, reloading")
        self.instrument = int(
            self.settings.value('instrument', DEFAULT_INSTRUMENT)
        )
        self.exercises = []
        self.settings.beginReadArray('exercises')
        for ex in self.settings.allKeys():
            if ex == 'size':
                continue
            self.exercises.append([
                ex,
                self.settings.value(ex)
            ])
        self.settings.endArray()
