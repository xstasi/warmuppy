import os
import tempfile
import gc
from warmuppy.mainwindow import mainwindow
from warmuppy.constants import DEFAULT_CUT, DEFAULT_BPM, DEFAULT_PREVIEW, DEFAULT_PROLONG

from pytestqt.qt_compat import qt_api # noqa
import pytest
from PySide2 import QtCore
from PySide2.QtWidgets import QRadioButton, QPushButton
from mido import MidiFile
from PySide2.QtCore import QCoreApplication as Application

midi_file = tempfile.NamedTemporaryFile().name

@pytest.fixture(autouse=True, scope='function')
def prepare():
    os.environ['WARMUPPY_KEEP_MIDI'] = midi_file
    os.environ['DEBUG'] = 'TRUE'
    os.environ['HOME'] = '/tmp/jaja'
    yield
    os.system('rm -rf /tmp/jaja')


@pytest.fixture(scope='function')
def prepare_play(qtbot):
    widget = mainwindow()
    widget.settings.clear()
    widget.show()
    qtbot.addWidget(widget)
    yield qtbot, widget
    widget.stop()
    widget.close()
    widget.close()
    del qtbot
    with open('/tmp/h2','a') as x:
        x.write(str(widget))
    del widget
    gc.collect()
    if os.path.isfile(midi_file):
        os.remove(midi_file)

def first_note(skip=0):
    mf = MidiFile(midi_file)
    track = mf.tracks[0]
    track.reverse()
    track.pop()  # program_change
    for x in range(0,skip):
        track.pop()
    return track.pop()


def click_note(self, octave, note):
    self.bot.mouseClick(
        self.widget.findChild(QRadioButton, f"radioButton_O{octave}"),
        QtCore.Qt.LeftButton
    )
    self.bot.mouseClick(
        self.widget.findChild(QRadioButton, f"radioButton_{note}"),
        QtCore.Qt.LeftButton
    )

def play(self, button='playButton'):
    self.bot.mouseClick(
        self.widget.findChild(QPushButton, button),
        QtCore.Qt.LeftButton
    )
    self.bot.waitSignal(self.widget.midi_ready_signal, timeout=1000)

def first_exercise(self):
    self.bot.mouseClick(self.widget.ui.comboExercise, QtCore.Qt.LeftButton)
    self.bot.keyClick(self.widget.ui.comboExercise, QtCore.Qt.Key_Home)

def last_exercise(self):
    self.bot.mouseClick(self.widget.ui.comboExercise, QtCore.Qt.LeftButton)
    self.bot.keyClick(self.widget.ui.comboExercise, QtCore.Qt.Key_End)


class TestBPM:
    def test_bpm_60(self,prepare_play):
        self.bot, self.widget = prepare_play
        self.bot.keyClicks(self.widget.ui.spinBPM, '60')

class TestPreview:
    def test_preview_prolongs_3(self,prepare_play):
        self.bot, self.widget = prepare_play
        self.bot.keyClicks(self.widget.ui.spinPreview, '3')
        if not DEFAULT_PREVIEW:
            self.bot.mouseClick(self.widget.ui.previewCheckBox, QtCore.Qt.LeftButton)
        play(self)
        x = first_note().time
        y = first_note(2).time 
        assert x == y * 3
    def test_preview_prolongs_2(self,prepare_play):
        self.bot, self.widget = prepare_play
        self.bot.keyClicks(self.widget.ui.spinPreview, '2')
        if not DEFAULT_PREVIEW:
            self.bot.mouseClick(self.widget.ui.previewCheckBox, QtCore.Qt.LeftButton)
        play(self)
        x = first_note().time
        y = first_note(2).time 
        assert x == y * 2
    def test_preview_toggles(self,prepare_play, qtlog):
        self.bot, self.widget = prepare_play
        self.bot.keyClicks(self.widget.ui.spinPreview, '2')
        if DEFAULT_PREVIEW:
            self.bot.mouseClick(self.widget.ui.previewCheckBox, QtCore.Qt.LeftButton)
        play(self)
        x = first_note().time
        y = first_note(2).time 
        assert x == y
#        assert qtlog.records == 0

class TestExercise:

    def test_select_first_exercise(self,prepare_play):
        self.bot, self.widget = prepare_play
        first_exercise(self)
        assert self.widget.exercise == 0
    def test_select_last_exercise(self,prepare_play):
        self.bot, self.widget = prepare_play
        last_exercise(self)
        assert self.widget.exercise == 1

    def test_first_exercise_right_note_C5(self,prepare_play):
        self.bot, self.widget = prepare_play
        click_note(self,5, 'C')
        first_exercise(self)
        play(self)
        assert first_note(skip=4).note == 84

class TestPlay:

    def test_play_creates_midi(self, prepare_play):
        self.bot, self.widget = prepare_play
        play(self)
        assert os.path.isfile(midi_file)

    def test_C5_plays_C5(self, prepare_play):
        self.bot, self.widget = prepare_play
        click_note(self, 5, 'C')
        play(self)
        assert first_note().note == 72

    def test_D5_plays_D5(self, prepare_play):
        self.bot, self.widget = prepare_play
        click_note(self, 5, 'D')
        play(self)
        assert first_note().note == 74

    def test_Cs5_plays_Cs5(self, prepare_play):
        self.bot, self.widget = prepare_play
        click_note(self, 5, 'Cs')
        play(self)
        assert first_note().note == 73

    def test_higher_E3_plays_F3(self, prepare_play):
        self.bot, self.widget = prepare_play
        click_note(self, 3, 'E')
        play(self,'higherButton')
        assert first_note().note == 53

    def test_higher_C5_plays_Cs5(self, prepare_play):
        self.bot, self.widget = prepare_play
        click_note(self,5, 'C')
        play(self,'higherButton')
        assert first_note().note == 73

    def test_lower_E3_plays_Ds3(self, prepare_play):
        self.bot, self.widget = prepare_play
        click_note(self, 3, 'E')
        play(self,'lowerButton')
        assert first_note().note == 51

    def test_lower_C5_plays_B5(self, prepare_play):
        self.bot, self.widget = prepare_play
        click_note(self, 5, 'C')
        play(self,'lowerButton')
        assert first_note().note == 71
