import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCompleter, QMessageBox, QCheckBox, QMainWindow, QWidget
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout,
    QLabel, QCheckBox, QSlider, QLineEdit 
)
from PyQt6.QtCore import Qt

class Ui_SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 150, 150)

        self.central_widget = QWidget(self)  # Create a QWidget for the central area
        #self.setCentralWidget(self.central_widget)  # Set central widget for the dialog

        # Create a layout for the central widget
        layout = QVBoxLayout(self.central_widget)

        self.checkbox_eyes = QCheckBox("All eyes are Deja Vu", self.central_widget)
        self.checkbox_eyes.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.checkbox_eyes.stateChanged.connect(lambda: self.checkbox_toggled)   
        layout.addWidget(self.checkbox_eyes)


        self.ui_value_label = QLabel("In-game UI scale: ", self.central_widget)
        self.ui_value_label.setObjectName("ui_value_label")
        layout.addWidget(self.ui_value_label)

        self.ingame_ui_slider = QSlider(Qt.Orientation.Horizontal, self.central_widget)
        self.ingame_ui_slider.setGeometry(10, 50, 200, 30)
        self.ingame_ui_slider.setRange(70, 100)
        self.ingame_ui_slider.setTickPosition(QSlider.TickPosition.TicksBelow)  # Tick marks below the slider
        self.ingame_ui_slider.setTickInterval(5)  # Tick marks every 10 units        
        self.ingame_ui_slider.valueChanged.connect(self.auto_set_slider)   
        layout.addWidget(self.ingame_ui_slider)

        self.ui_value_label = QLabel(self.central_widget)

        self.save_button = QPushButton("Apply", self.central_widget)
        layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_settings)

        self.reset_button = QPushButton("Reset", self.central_widget)
        layout.addWidget(self.reset_button)
        self.reset_button.clicked.connect(self.reset_settings)
        
        self.reset_settings()

    def reset_settings(self):
        try:
            with open("settings.txt", "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        key, value = line.strip().split("=")
                        if key == "ingame_ui_scale":
                            self.ingame_ui_slider.setValue(int(value))
                        elif key == "all_eyes_are_dejavu":
                            self.checkbox_eyes.setChecked(value == "True")
        except Exception as e:
            pass


    def save_settings(self):
        try:
            with open("settings.txt", "w") as f:
                self.auto_set_slider(self.ingame_ui_slider.value())
                f.write(f"ingame_ui_scale={self.ingame_ui_slider.value()}\n")
                f.write(f"all_eyes_are_dejavu={self.checkbox_eyes.isChecked()}\n")

            success_message = QMessageBox(self)  # Create a QMessageBox
            success_message.setWindowTitle("Success")  # Set title
            success_message.setText("Settings saved successfully.")  # Set message text
            success_message.setIcon(QMessageBox.Icon.Information)  # Set icon
            success_message.setStandardButtons(QMessageBox.StandardButton.Ok)  # Add Ok button
            success_message.exec()  # Show the message box
        except Exception as e:
            error_message = QMessageBox(self)
            error_message.setWindowTitle("Error")
            error_message.setText("An error occurred while saving the settings.")
            error_message.setIcon(QMessageBox.Icon.Critical)
            error_message.setStandardButtons(QMessageBox.StandardButton.Ok)

    def auto_set_slider(self, value):
        if value < 73:
            value = 70
        elif value < 78:
            value = 75
        elif value < 83:
            value = 80
        elif value < 88:
            value = 85
        elif value < 93:
            value = 90
        elif value < 98:
            value = 95
        else:
            value = 100
        self.display(value)

    def display(self, value):
        self.central_widget.findChild(QtWidgets.QLabel, "ui_value_label").setText("In-game UI scale: " + str(value))
        self.ingame_ui_slider.setValue(value)

    def checkbox_toggled(value, state):
        global always_dejavu
        if state == Qt.CheckState.Checked.value:
            always_dejavu = True
            print("Always Deja Vu is now True")

        elif state == Qt.CheckState.Unchecked.value:
            always_dejavu = False
            print("Always Deja Vu is now False")

def load_settings(self):
        global always_dejavu, ui_scale
        try:
            with open("settings.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    key, value = line.strip().split("=")
                    if key == "ingame_ui_scale":
                        ui_scale = int(value)
                    elif key == "all_eyes_are_dejavu": 
                        always_dejavu = bool(value) 
                return ui_scale, always_dejavu
        except Exception as e:
            pass