import sys
import math
import threading
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTextEdit, QHBoxLayout, QLineEdit, QPushButton
from PyQt5.QtGui import QPainter, QColor, QFont, QRadialGradient, QBrush, QPixmap, QCursor
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject, QMetaType
from assistant import run_assistant

# Register QTextCursor for thread-safe communication
from PyQt5.QtGui import QTextCursor
QMetaType.type("QTextCursor")

class AssistantSignals(QObject):
    """Signals for thread-safe communication with GUI"""
    status_update = pyqtSignal(str)
    output_update = pyqtSignal(str)

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
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

        # Text Input Section
        input_layout = QHBoxLayout()
        
        # Text Input Field
        self.text_input = QLineEdit()
        self.text_input.setFont(QFont("Arial", 12))
        self.text_input.setStyleSheet("""
            QLineEdit {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 2px solid #39ff14;
                border-radius: 10px;
                padding: 8px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #00ffff;
            }
        """)
        self.text_input.setPlaceholderText("Type your command here...")
        self.text_input.returnPressed.connect(self.send_text_command)
        input_layout.addWidget(self.text_input)
        
        # Send Button
        self.send_button = QPushButton("Send")
        self.send_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #39ff14;
                color: #000000;
                border: none;
                border-radius: 10px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00ffff;
                color: #000000;
            }
            QPushButton:pressed {
                background-color: #00ff00;
            }
        """)
        self.send_button.clicked.connect(self.send_text_command)
        input_layout.addWidget(self.send_button)
        
        layout.addLayout(input_layout)

        # Footer
        self.footer = QLabel("Created By : Sanket")
        self.footer.setFont(QFont("Arial", 11, QFont.Bold))
        self.footer.setStyleSheet("color: #ff4d4d; background-color: transparent;")
        self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.footer)

        self.setLayout(layout)
        self.listening_thread = None
        self.active = False
        self.assistant_callback = None
        
        # Set up signals for thread-safe communication
        self.signals = AssistantSignals()
        self.signals.status_update.connect(self.update_status)
        self.signals.output_update.connect(self.update_output)

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
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - radius - 60, center_y - radius - 60,
                            (radius + 60) * 2, (radius + 60) * 2)

    def update_status(self, message):
        self.status_label.setText(f"Status: {message}")

    def update_output(self, message):
        self.output_area.append(message)

    def send_text_command(self):
        """Handle text input commands"""
        text = self.text_input.text().strip()
        if text:
            # Display user input
            self.update_output(f"You: {text}")
            self.text_input.clear()
            
            # Update status
            self.update_status("Processing text command...")
            
            # If assistant callback is available, use it
            if self.assistant_callback:
                try:
                    # Call the assistant with the text command
                    result = self.assistant_callback(text)
                    if result == "exit":
                        self.close_app()
                except Exception as e:
                    self.update_output(f"Error processing command: {str(e)}")
                    self.update_status("Error")
            else:
                self.update_output("Assistant not ready yet. Please wait...")

    def toggle_listening(self, event):
        if not self.active:
            self.start_assistant()

    def start_assistant(self):
        if not self.active:
            self.active = True
            self.update_status("Starting assistant...")
            
            # Use signals for thread-safe communication
            self.listening_thread = threading.Thread(
                target=run_assistant,
                args=(self.signals.status_update.emit, self.signals.output_update.emit, self.close_app, self.set_assistant_callback),
                daemon=True
            )
            self.listening_thread.start()

    def set_assistant_callback(self, callback):
        """Set the callback function for text commands"""
        self.assistant_callback = callback

    def close_app(self):
        self.update_status("Exiting...")
        app = QApplication.instance()
        if app:
            app.quit()
        os._exit(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoiceAssistantGUI()
    window.show()
    sys.exit(app.exec_())
