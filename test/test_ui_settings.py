import os
import tempfile

from warmuppy.ui.settings_window import SettingsWindow
from warmuppy.constants import APPLICATION_NAME
from pytestqt.qt_compat import qt_api  # noqa
import pytest
from PySide2 import QtCore

from mido import MidiFile

midi_file = tempfile.NamedTemporaryFile().name


# Load some defaults, launch the program, prepare qtbot and let the test run
@pytest.fixture
def prepare_main(qtbot):
    temp_home = tempfile.TemporaryDirectory()
    os.environ['HOME'] = temp_home.name
    os.environ['WARMUPPY_KEEP_MIDI'] = midi_file
    QtCore.QCoreApplication.setOrganizationName(APPLICATION_NAME)
    QtCore.QCoreApplication.setApplicationName(APPLICATION_NAME)
    q_settings = QtCore.QSettings()
    q_settings.setValue('instrument', 123)
    q_settings.beginWriteArray('exercises')
    q_settings.setValue('sample1', [1, 2, 3])
    q_settings.setValue('sample2', [4, 5, 6])
    q_settings.endArray()
    q_settings.sync()
    widget = SettingsWindow()
    widget.show()
    qtbot.addWidget(widget)
    yield qtbot, widget
    widget.close()


# TODO: find a way to test the exercise editor
class TestExercise:
    def test_remove_removes(self, prepare_main):
        self.bot, self.widget = prepare_main
        self.widget.ui.tabWidget.setCurrentIndex(0)
        self.widget.ui.exerciseList.setCurrentRow(0)
        exercise_count = self.widget.ui.exerciseList.count()
        self.bot.mouseClick(
            self.widget.ui.removeButton,
            QtCore.Qt.LeftButton
        )
        assert self.widget.ui.exerciseList.count() == exercise_count - 1


class TestSave:
    def test_removal_is_saved(self, prepare_main):
        self.bot, self.widget = prepare_main
        self.widget.ui.tabWidget.setCurrentIndex(0)
        self.widget.ui.exerciseList.setCurrentRow(0)
        self.bot.mouseClick(
            self.widget.ui.removeButton,
            QtCore.Qt.LeftButton
        )
        self.bot.mouseClick(
            self.widget.ui.saveButton,
            QtCore.Qt.LeftButton
        )
        saved_exercises = []
        q_settings = QtCore.QSettings()
        q_settings.beginReadArray('exercises')
        for ex in q_settings.allKeys():
            if ex == 'size':
                continue
            saved_exercises.append([
                ex,
                q_settings.value(ex)
            ])
        q_settings.endArray()
        assert saved_exercises == [
            ['sample2', [4, 5, 6]]
        ]
        assert self.bot.waitSignal(self.widget.settings_signal, timeout=1000)


class TestInstrument:
    def test_preview_plays_1(self, prepare_main):
        self.bot, self.widget = prepare_main
        self.widget.ui.tabWidget.setCurrentIndex(1)
        self.widget.ui.instrumentList.setCurrentRow(1)
        self.bot.mouseClick(
            self.widget.ui.previewButton,
            QtCore.Qt.LeftButton
        )
        mf = MidiFile(midi_file)
        track = mf.tracks[0]
        track.reverse()
        message = track.pop()  # program_change
        assert message.program == 1

    def test_preview_plays_5(self, prepare_main):
        self.bot, self.widget = prepare_main
        self.widget.ui.tabWidget.setCurrentIndex(1)
        self.widget.ui.instrumentList.setCurrentRow(5)
        self.bot.mouseClick(
            self.widget.ui.previewButton,
            QtCore.Qt.LeftButton
        )
        mf = MidiFile(midi_file)
        track = mf.tracks[0]
        track.reverse()
        message = track.pop()  # program_change
        assert message.program == 5
