import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTextEdit
from PyQt5.QtGui import QFont, QPixmap, QCursor
from PyQt5.QtCore import Qt
from assistant import run_assistant
import os

class VoiceAssistantGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Futuristic Voice Assistant")
        self.setGeometry(300, 200, 700, 500)
        self.setStyleSheet("background-color: #1e1e2f; color: #39ff14;")

        layout = QVBoxLayout()

        self.title_label = QLabel("🤖 Virtual Assistant")
        self.title_label.setFont(QFont("Orbitron", 24))
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        self.status_label = QLabel("Status: Idle")
        self.status_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.status_label)

        self.output_area = QTextEdit()
        self.output_area.setFont(QFont("Consolas", 11))
        self.output_area.setStyleSheet("background-color: #2a2a3d; color: #a8ff60;")
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)

        self.mic_label = QLabel()
        self.mic_label.setAlignment(Qt.AlignCenter)
        self.mic_label.setPixmap(QPixmap("voice.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.mic_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.mic_label.mousePressEvent = self.toggle_listening
        layout.addWidget(self.mic_label)

        self.setLayout(layout)
        self.listening_thread = None
        self.active = False

    def update_status(self, message):
        self.status_label.setText(f"Status: {message}")

    def update_output(self, message):
        self.output_area.append(message)

    def toggle_listening(self, event):
        if not self.active:
            self.active = True
            self.listening_thread = threading.Thread(
                target=run_assistant,
                args=(self.update_status, self.update_output, self.close_app),
                daemon=True
            )
            self.listening_thread.start()


    def close_app(self):
        self.update_status("Exiting...")
        QApplication.instance().quit()
        os._exit(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoiceAssistantGUI()
    window.show()
    sys.exit(app.exec_())
