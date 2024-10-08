import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCompleter, QMessageBox, QCheckBox, QMainWindow, QWidget
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout,
    QLabel, QCheckBox, QSlider, QLineEdit 
)
from PyQt6.QtCore import Qt

always_dejavu = False
ui_scale = 75

class Ui_SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 300, 200)

        self.central_widget = QWidget(self)  # Create a QWidget for the central area
        #self.setCentralWidget(self.central_widget)  # Set central widget for the dialog

        # Create a layout for the central widget
        layout = QVBoxLayout(self.central_widget)

        self.checkbox_eyes = QCheckBox("All eyes are Deja Vu", self.central_widget)
        self.checkbox_eyes.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.checkbox_eyes.stateChanged.connect(lambda: self.checkbox_toggled)   
        layout.addWidget(self.checkbox_eyes)

        self.ui_value_label = QLabel("In-game UI scale: " + str(ui_scale),  self.central_widget)
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

    def checkbox_toggled(value, state):
        always_dejavu

        if state == Qt.CheckState.Checked.value:
            always_dejavu = True
            print("Always Deja Vu is now True")

        elif state == Qt.CheckState.Unchecked.value:
            always_dejavu = False
            print("Always Deja Vu is now False")
