from PyQt5 import QtWidgets
import sys
from design.interface import Ui_MainWindow
from recorder_thread import RecorderThread

class KamenBotApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(KamenBotApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.recording = False
        self.ui.RecordAudio.clicked.connect(self.toggle_recording)

        self.recorder_thread = RecorderThread()
        self.recorder_thread.finished.connect(self.on_recording_finished)

    def toggle_recording(self):
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        self.recording = True
        self.ui.RecordAudio.setText("Stop Audio")

        self.recorder_thread.recording = True
        self.recorder_thread.start()

    def stop_recording(self):
        self.recording = False
        self.ui.RecordAudio.setText("Record Audio")

        self.recorder_thread.stop()

        self.recorder_thread.wait()
        self.recorder_thread.save_audio()

    def on_recording_finished(self):
        self.recorder_thread.save_audio()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = KamenBotApp()
    window.show()
    app.exec_()
