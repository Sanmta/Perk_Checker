from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QCheckBox, QSlider, QLineEdit
from PyQt6.QtCore import Qt


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 300, 200)

        # Create a layout
        layout = QVBoxLayout()

        # Add widgets to the settings window
        layout.addWidget(QLabel("Enable feature:"))
        self.feature_checkbox = QCheckBox("Enable cool feature", self)
        layout.addWidget(self.feature_checkbox)

        layout.addWidget(QLabel("Adjust volume:"))
        self.volume_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.volume_slider.setRange(0, 100)
        layout.addWidget(self.volume_slider)

        layout.addWidget(QLabel("Enter username:"))
        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_input)

        # Set the dialog layout
        self.setLayout(layout)