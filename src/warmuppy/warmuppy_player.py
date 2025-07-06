import time
import threading
import subprocess
import tempfile
import os
import wave
import pygame


class WarmuppyPlayer:
    def __init__(self):
        pygame.mixer.init(buffer=44100)  # bigger buffer        self._soundfont = "/usr/share/soundfonts/default.sf2"
        self._duration = 0
        self._start_time = 0
        self._play_thread = None
        self._stop_flag = threading.Event()
        self._lock = threading.Lock()
        self._temp_wav_path = None
        self._soundfont = '/usr/share/soundfonts/default.sf2'

    def _convert_midi_to_wav(self, midi_path):
        fd, wav_path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        subprocess.run([
            "fluidsynth", "-ni", self._soundfont, midi_path,
            "-F", wav_path, "-r", "44100"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return wav_path

    def _get_wav_duration(self, wav_path):
        with wave.open(wav_path, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return frames / float(rate)

    def _play_wav(self, wav_path):
        self._stop_flag.clear()
        self._duration = self._get_wav_duration(wav_path)
        self._start_time = time.time()
        pygame.mixer.music.load(wav_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            if self._stop_flag.is_set():
                pygame.mixer.music.stop()
                break
            time.sleep(0.1)

        # Clean up
        if os.path.exists(wav_path):
            os.remove(wav_path)
        self._temp_wav_path = None

    def play(self, midi_path):
        self.stop()
        self._temp_wav_path = self._convert_midi_to_wav(midi_path)
        self._play_thread = threading.Thread(target=self._play_wav, args=(self._temp_wav_path,), daemon=True)
        self._play_thread.start()

    def stop(self):
        self._stop_flag.set()
        pygame.mixer.music.stop()
        if self._play_thread and self._play_thread.is_alive():
            self._play_thread.join()
        if self._temp_wav_path and os.path.exists(self._temp_wav_path):
            os.remove(self._temp_wav_path)
            self._temp_wav_path = None

    def is_playing(self):
        return pygame.mixer.music.get_busy()

    def get_progress(self):
        if not self.is_playing() or self._duration == 0:
            return 0.0
        elapsed = time.time() - self._start_time
        return round(min(elapsed / self._duration, 1.0) * 100, 1)
