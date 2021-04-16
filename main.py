import sys
import os

import pygame
import tempfile
import logging

from ui.mainwindow import Ui_MainWindow
from ui.howto import Ui_Howto
from ui.about import Ui_About
from settings import settingswindow

from PySide2.QtWidgets import (
    QApplication, QMainWindow, QRadioButton, QStyle, QDialog
)
from PySide2.QtCore import QTimer, QSettings, QCoreApplication, Signal

from mido import Message, MidiFile, MidiTrack

pygame.init()

APPLICATION_NAME = 'Warmuppy'
APPLICATION_VERSION = '0.1'

NOTES = [
    "C",
    "Cs",
    "D",
    "Ds",
    "E",
    "F",
    "Fs",
    "G",
    "Gs",
    "A",
    "As",
    "B",
]

if os.getenv("DEBUG") == 'TRUE':
    logging.basicConfig(level=logging.DEBUG)

DEFAULT_BPM = 100
DEFAULT_CUT = 0.02
DEFAULT_STEP = 1
DEFAULT_EXERCISES = [
    ["Scale up/down, 2 steps", [0, 2, 4, 2, 0]],
    ["Octave up/down", [0, 12, 0]],
]
DEFAULT_EXERCISE = 0
DEFAULT_PREVIEW = True
DEFAULT_PREVIEW_TIME = 3
DEFAULT_PROLONG = True
DEFAULT_PROLONG_TIME = 3
DEFAULT_INSTRUMENT = 0

NOTE_CHAN = 0

EXERCISE = 0


class aboutwindow(QDialog):
    def __init__(self, parent=None):
        super(aboutwindow, self).__init__()
        self.ui = Ui_About()
        self.ui.setupUi(self)
        self.ui.labelNameVersion.setText(
            f"{APPLICATION_NAME} {APPLICATION_VERSION}"
        )
        self.ui.pushButton.clicked.connect(self.accept)


class howtowindow(QDialog):
    def __init__(self, parent=None):
        super(howtowindow, self).__init__()
        self.ui = Ui_Howto()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.accept)


class mainwindow(QMainWindow):

    settings_signal = Signal()

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
        self.ui.setupUi(self)

        # Restyle buttons to use QT builtin icons,
        #  which cannot be done on qtdesigner
        self.ui.playButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay)
        )
        # self.ui.playButton.setText('')
        self.ui.stopButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaStop)
        )
        # self.ui.stopButton.setText('')
        self.ui.lowerButton.setIcon(
            self.style().standardIcon(QStyle.SP_ArrowDown)
        )
        # self.ui.lowerButton.setText('')
        self.ui.higherButton.setIcon(
            self.style().standardIcon(QStyle.SP_ArrowUp)
        )
        # self.ui.higherButton.setText('')

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
        print(self.exercise)
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

    def bump_note(self, up):
        self.stop()
        base_note = 24 + (self.octave - 1) * 12 + self.note
        logging.debug(f"Current note: {base_note}")
        max = 8 * 12 + 24
        min = 25
        if up:
            if base_note < max:
                base_note += self.step
        else:
            if base_note > min:
                base_note -= self.step

        octave = (base_note - 24) // 12 + 1
        logging.debug(f"New note: {base_note}")
        logging.debug(f"New octave should be #{octave}")
        octave_radio = self.findChild(QRadioButton, f"radioButton_O{octave}")
        octave_radio.setChecked(True)
        note_id = (base_note - 24) % 12
        note = self.notes[note_id]
        logging.debug(f"New note should be #{note}")
        note_radio = self.findChild(QRadioButton, f"radioButton_{note}")
        note_radio.setChecked(True)
        self.play_exercise()

    def play_exercise(self):
        self.stop()
        midi_file = tempfile.NamedTemporaryFile(delete=False)
        ex = self.exercises[self.exercise]
        name = ex[0]
        seq = ex[1]
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)
        track.append(
            Message('program_change', program=self.instrument, time=0)
        )
        logging.debug(f"Starting exercise '{name}' (pattern: {seq})")
        self.ui.progressBar.setValue(0)
        base_note = 24 + (self.octave - 1) * 12 + self.note
        seconds = 60 / self.bpm
        duration = (seconds - self.cut) * 1000
        timer_delay = 0
        if self.preview:
            timer_delay = int(duration*self.preview_time)
            track.append(
                Message('note_on', note=(base_note), velocity=100, time=0)
            )
            track.append(
                Message('note_off', note=(base_note), time=timer_delay)
            )
        for idx, p in enumerate(seq):
            p = int(p)
            i = idx + 1
            percent = (i / len(seq)) * 100
            self.timers.append(QTimer())
            timer = self.timers[-1]
            timer.setSingleShot(True)
            if idx == (len(seq) - 1) and self.prolong:
                logging.debug(f"prolonging {p}")
                delay = int(duration*self.prolong_time)
            else:
                delay = int(duration)
            track.append(
                Message('note_on', note=(base_note+p), velocity=100, time=0)
            )
            track.append(
                Message('note_off', note=(base_note+p), time=delay)
            )
            timer.timeout.connect(
                lambda pc=percent: self.ui.progressBar.setValue(pc)
            )
            logging.debug(f"Starting timer for {percent}% after {delay}ms")
            timer.start(timer_delay + duration*idx)
        mid.save(file=midi_file)
        midi_file.flush()
        midi_file.close()
        pygame.mixer.music.load(midi_file.name)
        pygame.mixer.music.play()
        os.remove(midi_file.name)

    def stop(self):
        for timer in self.timers:
            timer.stop()
        self.ui.progressBar.setValue(0)
        pygame.mixer.music.stop()

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


if __name__ == "__main__":
    app = QApplication([])
    QCoreApplication.setOrganizationName(APPLICATION_NAME)
    QCoreApplication.setApplicationName(APPLICATION_NAME)
    widget = mainwindow()
    widget.show()
    sys.exit(app.exec_())
