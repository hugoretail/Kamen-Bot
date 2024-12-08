import sys
from PyQt5 import QtWidgets
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from design.interface import Ui_MainWindow
from recorder_thread import RecorderThread
from openai import OpenAI

class KamenBotApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(KamenBotApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.recording = False
        self.ui.RecordAudio.clicked.connect(self.toggle_recording)

        self.recorder_thread = RecorderThread()
        self.recorder_thread.finished.connect(self.on_recording_finished)

        self.client = OpenAI()

        self.player = QMediaPlayer(self)

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

    def on_recording_finished(self):
        self.recorder_thread.save_audio()
        transcription = self.apply_stt()
        chat_response = self.send_prompt(transcription)
        self.apply_tts(chat_response)
        self.ui.DiscussionHistory.setText(chat_response)
        self.play_audio()

    def apply_stt(self):
        audio_file = open("./records/record.wav", "rb")
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return transcription
    
    def send_prompt(self, transcription):
        user_message = transcription.text
        system_message = f"You talk to the user in the same language. Adapt to their way of speaking and their manners."
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        chat_response = response['choices'][0]['message']['content']
        print("Chat response:", chat_response)
        return chat_response


    def apply_tts(self, chat_response):
        speech_path = "./speeches/speech.mp3"
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=chat_response
        )
        with open(speech_path, 'wb') as speech_file:
            for chunk in response.with_streaming_response():
                speech_file.write(chunk)

    def play_audio(self):
        speech_path = "./speeches/speech.mp3"
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(speech_path)))
        self.player.play()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = KamenBotApp()
    window.show()
    app.exec_()
