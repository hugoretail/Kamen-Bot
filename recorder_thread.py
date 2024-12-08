from pvrecorder import PvRecorder
from PyQt5.QtCore import QThread, pyqtSignal
import wave
import struct

class RecorderThread(QThread):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.recorder = PvRecorder(device_index=1, frame_length=512)
        self.recording = False
        self.audio = []

    def run(self):
        self.audio = []
        self.recorder.start()

        while self.recording:
            frame = self.recorder.read()
            self.audio.extend(frame)

        self.recorder.stop()
        self.finished.emit()

    def stop(self):
        self.recording = False

    def save_audio(self, filename="record.wav"):
        with wave.open("./records/" + filename, 'w') as f:
            f.setparams((1, 2, 16000, 512, "NONE", "NOBE"))
            f.writeframes(struct.pack("h" * len(self.audio), *self.audio))
