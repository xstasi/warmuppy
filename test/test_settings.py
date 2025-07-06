import os
import tempfile
import pygame

import pytest

from warmuppy.settings import Settings
from warmuppy.constants import APPLICATION_NAME

from PySide6.QtCore import QSettings
from PySide6.QtCore import QCoreApplication

from mido import MidiFile


@pytest.fixture(scope='function')
def temp_settings():
    temp_home = tempfile.TemporaryDirectory()
    os.environ['HOME'] = temp_home.name
    QCoreApplication.setOrganizationName(APPLICATION_NAME)
    QCoreApplication.setApplicationName(APPLICATION_NAME)
    q_settings = QSettings()
    q_settings.setValue('instrument', 123)
    q_settings.beginWriteArray('exercises')
    q_settings.setValue('sample1', ['1', '2', '3'])
    q_settings.setValue('sample2', ['4', '5', '6'])
    q_settings.endArray()
    q_settings.sync()
    settings = Settings()
    yield settings


class TestSettings:

    def test_reads_settings(self, temp_settings):
        settings = temp_settings
        assert settings.instrument == 123
        assert settings.exercises == [
            ['sample1', ['1', '2', '3']],
            ['sample2', ['4', '5', '6']]
        ]

    def test_set_instrument(self, temp_settings):
        settings = temp_settings
        settings.set_instrument(100)
        assert settings.instrument == 100

    def test_remove_exercise_1(self, temp_settings):
        settings = temp_settings
        settings.remove_exercise('sample1')
        assert settings.exercises == [
            ['sample2', ['4', '5', '6']]
        ]

    def test_remove_exercise_2(self, temp_settings):
        settings = temp_settings
        settings.remove_exercise('sample2')
        assert settings.exercises == [
            ['sample1', ['1', '2', '3']]
        ]

    def test_reload_exercise_1(self, temp_settings):
        settings = temp_settings
        settings.reload_exercise('sample1', '2 2 2')
        assert settings.exercises == [
            ['sample1', ['2', '2', '2']],
            ['sample2', ['4', '5', '6']]
        ]

    def test_reload_exercise_2(self, temp_settings):
        settings = temp_settings
        settings.reload_exercise('sample2', '3 3 3')
        assert settings.exercises == [
            ['sample1', ['1', '2', '3']],
            ['sample2', ['3', '3', '3']]
        ]

    def test_save_settings(self, temp_settings):
        settings = temp_settings
        settings.exercises = [
            ['sample3', [0, 0, 0]]
        ]
        settings.instrument = 99
        settings.save_settings()

        q_settings = QSettings()
        saved_instrument = q_settings.value('instrument')
        saved_exercises = []
        q_settings.beginReadArray('exercises')
        for ex in q_settings.allKeys():
            if ex == 'size':
                continue
            saved_exercises.append([
                ex,
                q_settings.value(ex)
            ])
        q_settings.endArray()

        assert saved_instrument == 99
        assert saved_exercises == [
            ['sample3', [0, 0, 0]]
        ]

    def test_preview_plays_something(self, temp_settings):
        settings = temp_settings
        settings.preview()
        assert pygame.mixer.music.get_busy() == 1

    def test_preview_plays_right_instrument(self, temp_settings):
        temp_midi = tempfile.NamedTemporaryFile()
        os.environ['WARMUPPY_KEEP_MIDI'] = temp_midi.name
        settings = temp_settings
        settings.instrument = 111
        settings.preview()
        pygame.mixer.music.stop()

        mf = MidiFile(temp_midi.name)
        track = mf.tracks[0]
        track.reverse()
        program_change = track.pop()
        assert program_change.program == 111
