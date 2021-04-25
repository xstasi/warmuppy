import os
import tempfile
import pytest
import pygame

from warmuppy.warmuppy import Warmuppy
from warmuppy.constants import APPLICATION_NAME
from warmuppy.constants import (
    DEFAULT_INSTRUMENT,
    DEFAULT_BPM, DEFAULT_CUT, DEFAULT_STEP, DEFAULT_PROLONG, DEFAULT_PREVIEW,
    DEFAULT_PREVIEW_TIME, DEFAULT_PROLONG_TIME,
)

from PySide2.QtCore import QSettings
from PySide2.QtCore import QCoreApplication

from mido import MidiFile


@pytest.fixture(autouse=True)
def temp_settings():
    temp_home = tempfile.TemporaryDirectory()
    os.environ['HOME'] = temp_home.name
    os.environ['WARMUPPY_DEBUG'] = 'TRUE'
    QCoreApplication.setOrganizationName(APPLICATION_NAME)
    QCoreApplication.setApplicationName(APPLICATION_NAME)
    app = Warmuppy()
    app.settings.sync()
    yield app, temp_home.name


def first_note(midi_file):
    mf = MidiFile(midi_file)
    track = mf.tracks[0]
    track.reverse()
    track.pop()  # program_change
    return track.pop().note


class TestBase:

    def test_creates_settings_dir(self, temp_settings):
        app, home = temp_settings
        conf = os.path.join(
            home,
            '.config',
            APPLICATION_NAME,
            f"{APPLICATION_NAME}.conf"
        )
        assert os.path.exists(conf)

    def test_loads_defaults(self, temp_settings):
        app, home = temp_settings
        assert app.bpm == DEFAULT_BPM
        assert app.cut == DEFAULT_CUT
        assert app.step == DEFAULT_STEP
        assert app.preview == DEFAULT_PREVIEW
        assert app.prolong == DEFAULT_PROLONG
        assert app.preview_time == DEFAULT_PREVIEW_TIME
        assert app.prolong_time == DEFAULT_PROLONG_TIME
        assert app.note == 0
        assert app.octave == 3
        assert app.instrument == DEFAULT_INSTRUMENT
        assert len(app.exercises) > 1

    def test_change_octave_4(self, temp_settings):
        app, home = temp_settings
        app.change_octave(4)
        app.settings.sync()
        assert app.octave == 4
        assert QSettings().value('octave') == 4

    def test_change_octave_5(self, temp_settings):
        app, home = temp_settings
        app.change_octave(5)
        assert app.octave == 5
        app.settings.sync()
        assert QSettings().value('octave') == 5

    def test_change_note_d(self, temp_settings):
        app, home = temp_settings
        app.change_note('D')
        assert app.note == 2
        assert QSettings().value('note') == 2

    def test_change_note_f(self, temp_settings):
        app, home = temp_settings
        app.change_note('F')
        assert app.note == 5
        assert QSettings().value('note') == 5

    def test_exercises_exist(self):
        settings_reader = QSettings()
        settings_reader.beginReadArray('exercises')
        assert len(settings_reader.allKeys()) > 1
        settings_reader.endArray()

    def test_change_exercise_0(self, temp_settings):
        app, home = temp_settings
        app.change_exercise(0)
        assert app.exercise == 0

    def test_change_exercise_1(self, temp_settings):
        app, home = temp_settings
        app.change_exercise(1)
        assert app.exercise == 1

    def test_change_exercise_out_of_bounds(self, temp_settings):
        app, home = temp_settings
        app.change_exercise(999)
        assert app.exercise == 0

    for x in "bpm cut step preview_time prolong_time".split():
        for i in [1, 99]:
            exec(f'''def test_change_{x}_{i}(self, temp_settings):
                        app, home = temp_settings
                        app.change_{x}({i})
                        assert app.{x} == {i}
                        assert QSettings().value('{x}') == {i}''')

    def test_change_preview_f(self, temp_settings):
        app, home = temp_settings
        app.change_preview(False)
        assert not app.preview
        assert not QSettings().value('preview')

    def test_change_preview_t(self, temp_settings):
        app, home = temp_settings
        app.change_preview(True)
        assert app.preview
        assert QSettings().value('preview')

    def test_change_prolong_f(self, temp_settings):
        app, home = temp_settings
        app.change_prolong(False)
        assert not app.prolong
        assert not QSettings().value('prolong')

    def test_change_prolong_t(self, temp_settings):
        app, home = temp_settings
        app.change_prolong(True)
        assert app.prolong
        assert QSettings().value('prolong')

    def test_higher_c5_plays_cs5(self, temp_settings):
        app, home = temp_settings
        app.change_note('C')
        app.change_octave(5)
        octave, note = app.bump_note(True)
        assert octave == 5
        assert note == 'Cs'

    def test_higher_b3_plays_c4(self, temp_settings):
        app, home = temp_settings
        app.change_note('B')
        app.change_octave(3)
        octave, note = app.bump_note(True)
        assert octave == 4
        assert note == 'C'

    def test_lower_cs5_plays_c5(self, temp_settings):
        app, home = temp_settings
        app.change_note('Cs')
        app.change_octave(5)
        octave, note = app.bump_note(False)
        assert octave == 5
        assert note == 'C'

    def test_lower_c4_plays_b3(self, temp_settings):
        app, home = temp_settings
        app.change_note('C')
        app.change_octave(4)
        octave, note = app.bump_note(False)
        assert octave == 3
        assert note == 'B'

    def test_play_plays_something(self, temp_settings):
        app, home = temp_settings
        app.play_exercise()
        assert pygame.mixer.music.get_busy() == 1

    def test_play_plays_right_exercise(self, temp_settings):
        temp_midi = tempfile.NamedTemporaryFile()
        os.environ['WARMUPPY_KEEP_MIDI'] = temp_midi.name
        app, home = temp_settings
        app.change_preview(False)
        app.change_note('E')
        app.change_octave(3)
        app.exercises = [
            ['sample1', [1]],
            ['sample2', [2]],
        ]
        app.change_exercise(0)
        app.play_exercise()
        app.stop()
        assert first_note(temp_midi.name) == 53
        app.change_exercise(1)
        app.play_exercise()
        app.stop()
        assert first_note(temp_midi.name) == 54

    def test_stop(self, temp_settings):
        app, home = temp_settings
        app.play_exercise()
        app.stop()
        assert pygame.mixer.music.get_busy() == 0

    def test_reload(self, temp_settings):
        app, home = temp_settings
        settings = QSettings()
        settings.clear()
        settings.setValue('instrument', 123)
        settings.beginWriteArray('exercises')
        settings.setValue('sample1', [1, 2, 3])
        settings.setValue('sample2', [4, 5, 6])
        settings.endArray()
        app.reload_settings()
        assert app.instrument == 123
        assert app.exercises == [
            ['sample1', [1, 2, 3]],
            ['sample2', [4, 5, 6]]
        ]
