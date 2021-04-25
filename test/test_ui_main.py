import os
import tempfile

from warmuppy.ui.warmuppy_window import WarmuppyWindow
from warmuppy.constants import DEFAULT_PREVIEW, DEFAULT_PROLONG, DEFAULT_CUT
from pytestqt.qt_compat import qt_api  # noqa
import pytest
from PySide2 import QtCore
from PySide2.QtWidgets import QRadioButton, QPushButton
from mido import MidiFile

midi_file = tempfile.NamedTemporaryFile().name


# Launch instances with midi persistence and ephemeral config
@pytest.fixture(autouse=True)
def prepare():
    os.environ['WARMUPPY_KEEP_MIDI'] = midi_file
    os.environ['HOME'] = ''


# Launch the program, prepare qtbot and let the test run
@pytest.fixture
def prepare_main(qtbot):
    widget = WarmuppyWindow()
    widget.show()
    qtbot.addWidget(widget)
    yield qtbot, widget
    widget.close()
    if os.path.isfile(midi_file):
        os.remove(midi_file)


@pytest.fixture
def prepare_play(prepare_main):
    bot, widget = prepare_main
    yield bot, widget
    widget.stop()


# Helper to get the first/last note of a midi file
def first_note(skip=0, rev=True):
    mf = MidiFile(midi_file)
    track = mf.tracks[0]
    # pop() gives us the last, so we reverse the track
    if rev:
        track.reverse()
        track.pop()  # program_change
    for x in range(0, skip):
        track.pop()
    return track.pop()


# Simulate clicking note/octave
def click_note(self, octave, note):
    self.bot.mouseClick(
        self.widget.findChild(QRadioButton, f"radioButton_O{octave}"),
        QtCore.Qt.LeftButton
    )
    self.bot.mouseClick(
        self.widget.findChild(QRadioButton, f"radioButton_{note}"),
        QtCore.Qt.LeftButton
    )


# Click play, optionally going higher or lower
def play(self, button='playButton'):
    self.bot.mouseClick(
        self.widget.findChild(QPushButton, button),
        QtCore.Qt.LeftButton
    )
    self.bot.waitSignal(self.widget.midi_ready_signal, timeout=1000)


# Helpers to select the first/last exercise
def first_exercise(self):
    self.bot.mouseClick(self.widget.ui.comboExercise, QtCore.Qt.LeftButton)
    self.bot.keyClick(self.widget.ui.comboExercise, QtCore.Qt.Key_Home)


def last_exercise(self):
    self.bot.mouseClick(self.widget.ui.comboExercise, QtCore.Qt.LeftButton)
    self.bot.keyClick(self.widget.ui.comboExercise, QtCore.Qt.Key_End)


# Toggling twice breaks on non-forked pytest, this intercepts it
class TestCanary:
    def test_preview_toggles_canary(self, prepare_play):
        self.bot, self.widget = prepare_play
        self.bot.keyClicks(self.widget.ui.spinPreview, '2')
        if DEFAULT_PREVIEW:
            self.bot.mouseClick(
                self.widget.ui.previewCheckBox,
                QtCore.Qt.LeftButton
            )
        play(self)
        x = first_note().time
        y = first_note(2).time
        assert x == y

    def test_preview_toggles_canary_2(self, prepare_play):
        self.bot, self.widget = prepare_play
        self.bot.keyClicks(self.widget.ui.spinPreview, '2')
        if DEFAULT_PREVIEW:
            self.bot.mouseClick(
                self.widget.ui.previewCheckBox,
                QtCore.Qt.LeftButton
            )
        play(self)
        x = first_note().time
        y = first_note(2).time
        assert x == y


class TestExercise:

    def test_select_first_exercise(self, prepare_play):
        self.bot, self.widget = prepare_play
        first_exercise(self)
        assert self.widget.exercise == 0

    def test_select_last_exercise(self, prepare_play):
        self.bot, self.widget = prepare_play
        last_exercise(self)
        assert self.widget.exercise == 1

    def test_first_exercise_right_note_c5(self, prepare_play):
        self.bot, self.widget = prepare_play
        click_note(self, 5, 'C')
        first_exercise(self)
        play(self)
        assert first_note(skip=4).note == 74

    def test_first_exercise_right_note_d5(self, prepare_play):
        self.bot, self.widget = prepare_play
        click_note(self, 5, 'D')
        first_exercise(self)
        play(self)
        assert first_note(skip=4).note == 76


class TestPlay:

    def test_play_creates_midi(self, prepare_play):
        self.bot, self.widget = prepare_play
        play(self)
        assert os.path.isfile(midi_file)

    def test_c5_plays_c5(self, prepare_play):
        self.bot, self.widget = prepare_play
        click_note(self, 5, 'C')
        play(self)
        assert first_note().note == 72

    def test_d5_plays_d5(self, prepare_play):
        self.bot, self.widget = prepare_play
        click_note(self, 5, 'D')
        play(self)
        assert first_note().note == 74

    def test_cs5_plays_cs5(self, prepare_play):
        self.bot, self.widget = prepare_play
        click_note(self, 5, 'Cs')
        play(self)
        assert first_note().note == 73

    def test_higher_e3_plays_f3(self, prepare_play):
        self.bot, self.widget = prepare_play
        click_note(self, 3, 'E')
        play(self, 'higherButton')
        assert first_note().note == 53

    def test_higher_c5_plays_cs5(self, prepare_play):
        self.bot, self.widget = prepare_play
        click_note(self, 5, 'C')
        play(self, 'higherButton')
        assert first_note().note == 73

    def test_lower_e3_plays_ds3(self, prepare_play):
        self.bot, self.widget = prepare_play
        click_note(self, 3, 'E')
        play(self, 'lowerButton')
        assert first_note().note == 51

    def test_lower_c5_plays_b5(self, prepare_play):
        self.bot, self.widget = prepare_play
        click_note(self, 5, 'C')
        play(self, 'lowerButton')
        assert first_note().note == 71


class TestPreview:
    def test_preview_prolongs_3(self, prepare_play):
        self.bot, self.widget = prepare_play
        self.bot.keyClicks(self.widget.ui.spinPreview, '3')
        if not DEFAULT_PREVIEW:
            self.bot.mouseClick(
                self.widget.ui.previewCheckBox,
                QtCore.Qt.LeftButton
            )
        play(self)
        x = first_note().time
        y = first_note(2).time
        assert x == y * 3

    def test_preview_prolongs_2(self, prepare_play):
        self.bot, self.widget = prepare_play
        self.bot.keyClicks(self.widget.ui.spinPreview, '2')
        if not DEFAULT_PREVIEW:
            self.bot.mouseClick(
                self.widget.ui.previewCheckBox,
                QtCore.Qt.LeftButton
            )
        play(self)
        x = first_note().time
        y = first_note(2).time
        assert x == y * 2

    def test_preview_toggles(self, prepare_play):
        self.bot, self.widget = prepare_play
        self.bot.keyClicks(self.widget.ui.spinPreview, '2')
        if DEFAULT_PREVIEW:
            self.bot.mouseClick(
                self.widget.ui.previewCheckBox,
                QtCore.Qt.LeftButton
            )
        play(self)
        x = first_note().time
        y = first_note(2).time
        assert x == y


class TestProlong:
    def test_prolong_prolongs_3(self, prepare_play):
        self.bot, self.widget = prepare_play
        self.bot.keyClicks(self.widget.ui.spinProlong, '3')
        self.widget.ui.spinBPM.setValue(60)
        self.widget.ui.spinCut.setValue(0)
        if not DEFAULT_PROLONG:
            self.bot.mouseClick(
                self.widget.ui.previewCheckBox,
                QtCore.Qt.LeftButton
            )
        play(self)
        x = first_note(skip=0, rev=False).time
        y = first_note(skip=2, rev=False).time
        assert x == y * 3

    def test_prolong_prolongs_2(self, prepare_play):
        self.bot, self.widget = prepare_play
        self.bot.keyClicks(self.widget.ui.spinProlong, '2')
        self.widget.ui.spinBPM.setValue(60)
        self.widget.ui.spinCut.setValue(0)
        if not DEFAULT_PROLONG:
            self.bot.mouseClick(
                self.widget.ui.previewCheckBox,
                QtCore.Qt.LeftButton
            )
        play(self)
        x = first_note(skip=0, rev=False).time
        y = first_note(skip=2, rev=False).time
        assert x == y * 2

    def test_preview_toggles(self, prepare_play):
        self.bot, self.widget = prepare_play
        if DEFAULT_PROLONG:
            self.bot.mouseClick(
                self.widget.ui.prolongCheckBox,
                QtCore.Qt.LeftButton
            )
        play(self)
        x = first_note(skip=0, rev=False).time
        y = first_note(skip=2, rev=False).time
        assert x == y


class TestBPM:
    def test_bpm_60(self, prepare_play):
        self.bot, self.widget = prepare_play
        # Cannot do this through qtbot unfortunately
        self.widget.ui.spinBPM.setValue(60)
        if DEFAULT_PREVIEW:
            self.bot.mouseClick(
                self.widget.ui.previewCheckBox,
                QtCore.Qt.LeftButton
            )
        if DEFAULT_CUT > 0:
            self.widget.ui.spinCut.setValue(0)
        play(self)
        assert first_note(1).time == 1000

    def test_bpm_30(self, prepare_play):
        self.bot, self.widget = prepare_play
        self.widget.ui.spinBPM.setValue(30)
        if DEFAULT_PREVIEW:
            self.bot.mouseClick(
                self.widget.ui.previewCheckBox,
                QtCore.Qt.LeftButton
            )
        if DEFAULT_CUT > 0:
            self.widget.ui.spinCut.setValue(0)
        play(self)
        assert first_note(1).time == 2000


class TestStep:
    def test_step_2(self, prepare_play):
        self.bot, self.widget = prepare_play
        self.widget.ui.spinStep.setValue(2)
        click_note(self, 3, 'F')  # 53
        play(self, button='higherButton')
        assert first_note().note == 55

    def test_step_4(self, prepare_play):
        self.bot, self.widget = prepare_play
        self.widget.ui.spinStep.setValue(4)
        click_note(self, 3, 'F')  # 53
        play(self, button='lowerButton')
        assert first_note().note == 49


class TestCut:
    def test_cut_05(self, prepare_play):
        self.bot, self.widget = prepare_play
        self.widget.ui.spinCut.setValue(0.05)
        self.widget.ui.spinBPM.setValue(60)
        if DEFAULT_PREVIEW:
            self.bot.mouseClick(
                self.widget.ui.previewCheckBox,
                QtCore.Qt.LeftButton
            )
        play(self)
        assert first_note(1).time == 950

    def test_cut_07(self, prepare_play):
        self.bot, self.widget = prepare_play
        self.widget.ui.spinCut.setValue(0.1)
        self.widget.ui.spinBPM.setValue(60)
        if DEFAULT_PREVIEW:
            self.bot.mouseClick(
                self.widget.ui.previewCheckBox,
                QtCore.Qt.LeftButton
            )
        play(self)
        assert first_note(1).time == 900
