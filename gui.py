import sys
import math
import threading
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTextEdit
from PyQt5.QtGui import QPainter, QColor, QFont, QRadialGradient, QBrush, QPixmap, QCursor
from PyQt5.QtCore import Qt, QTimer
from assistant import run_assistant

class VoiceAssistantGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("A.U.R.A Virtual Assistant")
        self.setGeometry(300, 200, 900, 600)
        self.setStyleSheet("background-color: #0a0a0a; color: #39ff14;")

        self.angle = 0  # For animation
        layout = QVBoxLayout()

        # Title
        self.title_label = QLabel("🤖 A.U.R.A")
        self.title_label.setFont(QFont("Orbitron", 32))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #00ffff; background-color: transparent;")
        layout.addWidget(self.title_label)

        # Status Label
        self.status_label = QLabel("Status: Idle")
        self.status_label.setFont(QFont("Arial", 14))
        self.status_label.setStyleSheet("color: #ffffff; background-color: transparent;")
        layout.addWidget(self.status_label)

        # Output Area (Transparent)
        self.output_area = QTextEdit()
        self.output_area.setFont(QFont("Consolas", 11))
        self.output_area.setStyleSheet("background: transparent; color: #a8ff60; border: 1px solid transparent;")
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)

        # Mic Icon
        self.mic_label = QLabel()
        self.mic_label.setAlignment(Qt.AlignCenter)
        self.mic_label.setPixmap(QPixmap("voice.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.mic_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.mic_label.mousePressEvent = self.toggle_listening
        layout.addWidget(self.mic_label)

        # Footer
        self.footer = QLabel("Created By : Sanket")
        self.footer.setFont(QFont("Arial", 11, QFont.Bold))
        self.footer.setStyleSheet("color: #ff4d4d; background-color: transparent;")
        self.footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.footer)

        self.setLayout(layout)
        self.listening_thread = None
        self.active = False

        # Animation Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)

        QTimer.singleShot(1000, self.start_assistant)

    def resizeEvent(self, event):
        self.update()

    def animate(self):
        self.angle = (self.angle + 1) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = min(self.width(), self.height()) // 5
        pulse = 80 + 40 * math.sin(math.radians(self.angle))

        gradient = QRadialGradient(center_x, center_y, radius + 60)
        gradient.setColorAt(0.0, QColor(0, 255, 255, int(pulse)))
        gradient.setColorAt(0.5, QColor(138, 43, 226, int(pulse * 0.8)))
        gradient.setColorAt(1.0, QColor(0, 0, 0, 0))

        brush = QBrush(gradient)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center_x - radius - 60, center_y - radius - 60,
                            (radius + 60) * 2, (radius + 60) * 2)

    def update_status(self, message):
        self.status_label.setText(f"Status: {message}")

    def update_output(self, message):
        self.output_area.append(message)

    def toggle_listening(self, event):
        if not self.active:
            self.start_assistant()

    def start_assistant(self):
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
