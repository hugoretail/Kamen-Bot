from PyQt5 import QtWidgets
import sys
from design.interface import Ui_MainWindow

class KamenBotApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(KamenBotApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.recording = False

        self.ui.RecordAudio.clicked.connect(self.toggle_discussion)

    def toggle_discussion(self):
        if not self.recording:
            self.recording = True
            self.ui.RecordAudio.setText("Stop Record")
        else:
            self.recording = False
            self.ui.RecordAudio.setText("Record Audio")



app = QtWidgets.QApplication(sys.argv)
window = KamenBotApp()
window.show()
app.exec_()