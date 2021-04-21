import pygame
import tempfile
import logging
import os

from shutil import copyfile

from PySide2.QtWidgets import (
    QMainWindow, QRadioButton, QStyle
)
from PySide2.QtCore import (
    QTimer, QSettings, Signal
)
from PySide2.QtGui import QIcon

from mido import Message, MidiFile, MidiTrack

from warmuppy.ui.mainwindow import Ui_MainWindow
from warmuppy.settings import settingswindow
from warmuppy.about import aboutwindow
from warmuppy.howto import howtowindow

from warmuppy.resources import resources # noqa
from warmuppy.constants import (
    NOTES, DEFAULT_INSTRUMENT, DEFAULT_EXERCISE, DEFAULT_EXERCISES,
    DEFAULT_BPM, DEFAULT_CUT, DEFAULT_STEP, DEFAULT_PROLONG, DEFAULT_PREVIEW,
    DEFAULT_PREVIEW_TIME, DEFAULT_PROLONG_TIME,
)


class mainwindow(QMainWindow):

    # Connected to the settings window, to know if they changed
    settings_signal = Signal()
    midi_ready_signal = Signal()

    def __init__(self):
        super(mainwindow, self).__init__()

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
        prol = self.settings.value('prolong', DEFAULT_PROLONG)
        self.prolong = prol in ['true', True]
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
        if self.exercises == []:
            self.settings.beginWriteArray('exercises')
            for ex in DEFAULT_EXERCISES:
                self.exercises.append(ex)
                self.settings.setValue(ex[0], ex[1])
            self.settings.endArray()
        self.exercise = DEFAULT_EXERCISE
        self.settings.setValue('instrument', self.instrument)

        # Load UI
        self.ui = Ui_MainWindow()
        self.setWindowIcon(QIcon(':/icons/icon.ico'))
        self.ui.setupUi(self)

        # Restyle buttons to use QT builtin icons,
        #  which cannot be done on qtdesigner
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
        # Sub-dialog signals
        self.settings_signal.connect(self.reload_settings)
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
        w = aboutwindow()
        w.exec_()

    def show_settings(self):
        w = settingswindow(parent=self)
        w.exec_()

    def show_howto(self):
        w = howtowindow()
        w.exec_()

    def change_note(self, note):
        note_id = self.notes.index(note)
        logging.debug(f"New note is {note} ({note_id})")
        self.note = note_id
        self.settings.setValue('note', note_id)

    def change_octave(self, oct):
        logging.debug(f"New octave is {oct}")
        self.octave = oct
        self.settings.setValue('octave', oct)

    def change_exercise(self, i):
        self.exercise = i
        if self.exercises == []:
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
        self.ui.spinPreview.setEnabled(p)
        self.preview = p
        self.settings.setValue('preview', p)

    def change_prolong(self, p):
        logging.debug(f"Setting prolong as {p}")
        self.ui.spinProlong.setEnabled(p)
        self.prolong = p
        self.settings.setValue('prolong', p)

    # Go {step} semitones up or down
    def bump_note(self, up):

        self.stop()

        # Beginning of 3rd octave + selected octave * semitones + note
        base_note = 24 + (self.octave - 1) * 12 + self.note
        logging.debug(f"Current note: {base_note}")
        # Highest playable note is the last of the 8th octave
        max = 8 * 12 + 24
        # Lowest is C3
        min = 25

        # Compute new note
        if up:
            if base_note < max:
                base_note += self.step
        else:
            if base_note > min:
                base_note -= self.step
        logging.debug(f"New note: {base_note}")

        # Compute new octave
        octave = (base_note - 24) // 12 + 1
        logging.debug(f"New octave should be #{octave}")
        octave_radio = self.findChild(QRadioButton, f"radioButton_O{octave}")
        octave_radio.setChecked(True)

        # Compute relative note for the UI
        note_id = (base_note - 24) % 12
        note = self.notes[note_id]
        logging.debug(f"New note should be #{note}")
        note_radio = self.findChild(QRadioButton, f"radioButton_{note}")
        note_radio.setChecked(True)

        self.play_exercise()

    # Generate a midi with the exercise and then play it
    def play_exercise(self):
        self.stop()

        # Load selected exercise
        ex = self.exercises[self.exercise]
        name = ex[0]
        seq = ex[1]
        logging.debug(f"Starting exercise '{name}' (pattern: {seq})")
        self.ui.progressBar.setValue(0)

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
                Message('note_on', note=(base_note), velocity=100, time=0)
            )
            track.append(
                Message('note_off', note=(base_note), time=timer_delay)
            )

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

            # Create a new timer for the progress bar
            self.timers.append(QTimer())
            timer = self.timers[-1]
            timer.setSingleShot(True)
            timer.timeout.connect(
                lambda pc=percent: self.ui.progressBar.setValue(pc)
            )

            logging.debug(f"Setting timer for {percent}% after {delay}ms")
            timer.setInterval(timer_delay + duration*idx)

            # Append the note to the midi
            track.append(
                Message('note_on', note=(base_note+step), velocity=100, time=0)
            )
            track.append(
                Message('note_off', note=(base_note+step), time=delay)
            )
        # Save midi file and load it with pygame separately,
        #   to avoid race conditions
        mid.save(file=midi_file)
        midi_file.flush()
        midi_file.close()
        self.midi_ready_signal.emit()
        pygame.mixer.music.load(midi_file.name)

        # Once midi is loaded, start the % timers and play it
        for timer in self.timers:
            timer.start()
        pygame.mixer.music.play()

        # Cleanup
        if 'WARMUPPY_KEEP_MIDI' in os.environ:
            midi_copy = os.environ['WARMUPPY_KEEP_MIDI']
            copyfile(midi_file.name, midi_copy)
        os.remove(midi_file.name)

    def stop(self):
        # Stop the music
        pygame.mixer.music.stop()
        # Stop all timers and delete them
        for timer in self.timers:
            timer.stop()
        self.timers = []
        # Reset progress
        self.ui.progressBar.setValue(0)

    # Settings window told us that something changed, so reload everything
    def reload_settings(self):
        logging.debug("Settings saved, reloading")
        self.instrument = int(
            self.settings.value('instrument', DEFAULT_INSTRUMENT)
        )
        self.exercises = []
        self.ui.comboExercise.clear()
        self.settings.beginReadArray('exercises')
        for ex in self.settings.allKeys():
            if ex == 'size':
                continue
            self.exercises.append([
                ex,
                self.settings.value(ex)
            ])
            self.ui.comboExercise.addItem(ex)
        self.settings.endArray()
