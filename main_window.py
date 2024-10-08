#!/usr/bin/env python

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

from settings_window import Ui_SettingsWindow, always_dejavu, ui_scale
from image_processing import search
from input_validation import find_aspect_ratio
from perk_check import check_perks, find_partial_builds
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCompleter, QMessageBox, QCheckBox, QMainWindow
from PIL import ImageGrab
import os
import cv2
import numpy as np

class Ui_MainWindow(QMainWindow):
    def setup_ui(self, MainWindow):
        # main window setup
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1100, 900)
        MainWindow.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        MainWindow.setWindowTitle("Dead by Daylight Perk Checker")
        MainWindow.setWindowIcon(QtGui.QIcon("assets/perk_checker.png"))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        create_background_label(self, 0, 0)

        # dictionary to hold line edit widgets
        self.line_edits = {
            'searchPerk_1_Build_1': 'lblPerk_1_Build_1', 
            'searchPerk_2_Build_1': 'lblPerk_2_Build_1', 
            'searchPerk_3_Build_1': 'lblPerk_3_Build_1', 
            'searchPerk_4_Build_1': 'lblPerk_4_Build_1',                 
            'searchPerk_1_Build_2': 'lblPerk_1_Build_2', 
            'searchPerk_2_Build_2': 'lblPerk_2_Build_2', 
            'searchPerk_3_Build_2': 'lblPerk_3_Build_2', 
            'searchPerk_4_Build_2': 'lblPerk_4_Build_2',
            'searchPerk_1_Build_3': 'lblPerk_1_Build_3', 
            'searchPerk_2_Build_3': 'lblPerk_2_Build_3', 
            'searchPerk_3_Build_3': 'lblPerk_3_Build_3', 
            'searchPerk_4_Build_3': 'lblPerk_4_Build_3',
            'searchPerk_1_Build_4': 'lblPerk_1_Build_4', 
            'searchPerk_2_Build_4': 'lblPerk_2_Build_4', 
            'searchPerk_3_Build_4': 'lblPerk_3_Build_4', 
            'searchPerk_4_Build_4': 'lblPerk_4_Build_4'
        }        
        
        for i in range(1, 5): 
            create_build_label(self, str(i), 279, 25 + 202*(i-1))

            for j in range(1, 5):
                create_perk_icon(self, str(j), str(i), 180*(j) + 80, 205*(i-1) + 85) 
                create_perk_search_bar(self, str(j), str(i), 180 * j + 80, 205*(i-1) + 58) 

        create_settings_cog(self)



        self.UI_scale_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.UI_scale_label.setGeometry(QtCore.QRect(70, 865, 200, 22))
        self.UI_scale_label.setObjectName("lblUIScale")
        self.UI_scale_label.setText("In-game UI Scale: ")

        self.UI_scale_input = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.UI_scale_input.setGeometry(QtCore.QRect(170, 865, 50, 22))
        self.UI_scale_input.setObjectName("txtUIScale")
        self.UI_scale_input.setText(str(ui_scale))

        btn_paste = create_button(self, 380, 850, 261, 31, "Check Perks")
        btn_reset = create_button(self, 660, 850, 171, 31, "Reset")

        btn_paste.clicked.connect(lambda: paste_image(self))
        btn_reset.clicked.connect(lambda: reset_perks(self))

        MainWindow.show()
        
        show_error_message("Warning", "This program should NOT replace manual perk checking, it is only a tool to assist in the process and it may give wrong results from time to time. Send me a Discord message @sanmta with any feature ideas or bugs you find. Happy perk checking!") 


# function to get an image from clipboard and search for perks
def paste_image(self):
    clipboard_image = ImageGrab.grabclipboard() # get image from clipboard

    if (clipboard_image is None):
        show_error_message("Error", "No image found in clipboard.")
        return
        
    if (find_aspect_ratio(clipboard_image) != 0.5625):
        show_error_message("Error", "Aspect ratio must be 16:9.")
        return

    if (clipboard_image.size[0] != 1920):
        clipboard_image = clipboard_image.resize((1920, 1080))
        

    end_screen_screenshot = cv2.cvtColor(np.array(clipboard_image), cv2.COLOR_RGB2BGR)
    create_perk_arrays(self, search(end_screen_screenshot, always_dejavu))

# function to create arrays of both selected perks and detected perks
def create_perk_arrays(self, perks):
    detected_build_survivor_1 = [perk.replace("iconPerks_", "").replace(".jpg", "").lower() for perk in perks[0:4]]
    detected_build_survivor_2 = [perk.replace("iconPerks_", "").replace(".jpg", "").lower() for perk in perks[4:8]]
    detected_build_survivor_3 = [perk.replace("iconPerks_", "").replace(".jpg", "").lower() for perk in perks[8:12]]
    detected_build_survivor_4 = [perk.replace("iconPerks_", "").replace(".jpg", "").lower() for perk in perks[12:16]]

    expected_build_survivor_1 = [
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_1_Build_1").text()).lower(),
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_2_Build_1").text()).lower(),
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_3_Build_1").text()).lower(),
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_4_Build_1").text()).lower()
    ]
    
    expected_build_survivor_2 = [
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_1_Build_2").text()).lower(), 
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_2_Build_2").text()).lower(), 
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_3_Build_2").text()).lower(), 
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_4_Build_2").text()).lower()
    ]
    
    expected_build_survivor_3 = [
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_1_Build_3").text()).lower(),
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_2_Build_3").text()).lower(),
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_3_Build_3").text()).lower(),
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_4_Build_3").text()).lower()
    ]

    expected_build_survivor_4 = [
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_1_Build_4").text()).lower(), 
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_2_Build_4").text()).lower(), 
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_3_Build_4").text()).lower(), 
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_4_Build_4").text()).lower()
    ]
    
    if check_perks(detected_build_survivor_1, detected_build_survivor_2, detected_build_survivor_3, detected_build_survivor_4, expected_build_survivor_1):
        set_perk_backgrounds(self, 1, True, None)
    else:
        set_perk_backgrounds(self, 1, False, find_partial_builds(detected_build_survivor_1, detected_build_survivor_2, detected_build_survivor_3, expected_build_survivor_1))
        show_error_message("Warning", "Perk mismatch in build 1.")

    if check_perks(detected_build_survivor_1, detected_build_survivor_2, detected_build_survivor_3, detected_build_survivor_4, expected_build_survivor_2):
        set_perk_backgrounds(self, 2, True, None)
    else:
        set_perk_backgrounds(self, 2, False, find_partial_builds(detected_build_survivor_1, detected_build_survivor_2, detected_build_survivor_3, expected_build_survivor_2))
        show_error_message("Warning", "Perk mismatch in build 2.")

    if check_perks(detected_build_survivor_1, detected_build_survivor_2, detected_build_survivor_3, detected_build_survivor_4, expected_build_survivor_3):
        set_perk_backgrounds(self, 3, True, None)
    else:
        set_perk_backgrounds(self, 3, False, find_partial_builds(detected_build_survivor_1, detected_build_survivor_2, detected_build_survivor_3, expected_build_survivor_3))
        show_error_message("Warning", "Perk mismatch in build 3.")

    if check_perks(detected_build_survivor_1, detected_build_survivor_2, detected_build_survivor_3, detected_build_survivor_4, expected_build_survivor_4):
        set_perk_backgrounds(self, 4, True, None)
    else:
        show_error_message("Warning", "Perk mismatch in build 4.")
        set_perk_backgrounds(self, 4, False, find_partial_builds(detected_build_survivor_1, detected_build_survivor_2, detected_build_survivor_3, expected_build_survivor_4))

# function to create the settings button
def create_settings_cog(self):
    self.settings_button = QtWidgets.QPushButton(parent=self.centralwidget)
    self.settings_button.setGeometry(QtCore.QRect(970, 20, 110, 110))
    self.settings_button.setObjectName("btnSettings")
    self.settings_button.setIcon(QtGui.QIcon("assets/settings_cog.png"))
    self.settings_button.setIconSize(QtCore.QSize(100, 100))
    # Make the button transparent except for the icon
    self.settings_button.setStyleSheet(""" 
                QPushButton {
                    border: none;            /* Remove border */
                    background-color: rgba(0, 0, 0, 0); /* Transparent background */
                }
                QPushButton:pressed {
                    background-color: rgba(0, 0, 0, 50); /* Slightly visible background on click */
                }
            """)
    self.settings_button.clicked.connect(lambda: open_settings_window(self))
    
# function to set the background of the perk icons, green being a correct perk and red being incorrect
def set_perk_backgrounds(self, survivor_number, correct, non_matching_values):
    if correct:    
        for perk_no in range(1, 5):
            perk_bg = self.centralwidget.findChild(QtWidgets.QLabel, "lblPerkBG_" + str(perk_no) + "_Build_" + str(survivor_number))
            perk_bg.setPixmap(QtGui.QPixmap("assets/perks/perkBGCorrect.png"))
    else:
        for perk_no in range(1, 5):
            if any(perk_no == i for i, _ in non_matching_values):            
                perk_bg = self.centralwidget.findChild(QtWidgets.QLabel, "lblPerkBG_" + str(perk_no) + "_Build_" + str(survivor_number))
                perk_bg.setPixmap(QtGui.QPixmap("assets/perks/perkBGIncorrect.png"))
            else:
                perk_bg = self.centralwidget.findChild(QtWidgets.QLabel, "lblPerkBG_" + str(perk_no) + "_Build_" + str(survivor_number))
                perk_bg.setPixmap(QtGui.QPixmap("assets/perks/perkBGCorrect.png"))

# function to show an error message
def show_error_message(title, message):
    message_box = QMessageBox()
    message_box.setIcon(QMessageBox.Icon.Critical)
    message_box.setWindowTitle(title)
    message_box.setText(message)
    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    message_box.exec()

# function to show a confirmation message
def show_are_you_sure_popup():
    # Create a QMessageBox
    msg_box = QMessageBox()

    # Set the icon, title, and text
    msg_box.setIcon(QMessageBox.Icon.Question)
    msg_box.setWindowTitle("Confirmation")
    msg_box.setText("Are you sure you want to proceed?")

    # Add buttons for the user to confirm or cancel the action
    msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

    # Execute the message box and return the user's response
    return msg_box.exec()



# function to create a background label
def create_background_label(self, x, y):
    _translate = QtCore.QCoreApplication.translate
    label_build = QtWidgets.QLabel(parent=self.centralwidget)
    label_build.setGeometry(QtCore.QRect(x, y, 1100, 900))
    label_build.setPixmap(QtGui.QPixmap("assets/main_background.png"))

# function to create a label for each build
def create_build_label(self, build_no, x, y):
    _translate = QtCore.QCoreApplication.translate
    label_build = QtWidgets.QLabel(parent=self.centralwidget)
    label_build.setGeometry(QtCore.QRect(x, y, 100, 22))
    font = QtGui.QFont()
    font.setFamily("Roboto Condensed")
    font.setBold(True)
    font.setPointSize(23)
    label_build.setFont(font)
    label_build.setObjectName("lblBuild_" + build_no)
    label_build.setText(_translate("MainWindow", "BUILD "  + build_no + ":"))

# function to create a perk icon for each perk
def create_perk_icon(self, perk_no, build_no, x, y):
    # create background for icon
    perk_icon_bg = QtWidgets.QLabel(parent=self.centralwidget)
    perk_icon_bg.setGeometry(QtCore.QRect(x, y, 125, 125))
    perk_icon_bg.setPixmap(QtGui.QPixmap("assets/perks/perkBG.png"))
    perk_icon_bg.setScaledContents(True)
    perk_icon_bg.setObjectName("lblPerkBG_" + perk_no + "_Build_" + build_no)
    # create icon on top of background
    perk_icon = QtWidgets.QLabel(parent=self.centralwidget)
    perk_icon.setGeometry(QtCore.QRect(x, y, 125, 125))
    perk_icon.setPixmap(QtGui.QPixmap(""))
    perk_icon.setScaledContents(True)
    perk_icon.setObjectName("lblPerk_" + perk_no + "_Build_" + build_no)     

# function to try and update the perk icon when the search bar is changed
def on_selection_changed(self, perk_search_bar):
    object_name = perk_search_bar.objectName()
    perk_no = object_name.split('_')[1]
    build_no = object_name.split('_')[3]
    # get the perk_icon object
    perk_icon = self.centralwidget.findChild(QtWidgets.QLabel, "lblPerk_" + perk_no + "_Build_" + build_no)
    try_icon_update(perk_search_bar, perk_icon)
    
# function to update perk icon when selection box changes
def try_icon_update(perk_search_bar, perk_icon):
    perk = format_perk_name(perk_search_bar.text())
    if (perk_exists(perk) == True):
        perk_icon.setPixmap(QtGui.QPixmap("assets/pngperks/iconPerks_" + perk + ".png"))
        perk_icon.show()
        return True
    else:
        perk_icon.hide()
        return False

# function to check if perk exists in the assets folder
def perk_exists(perk_name):
    if (os.path.exists("assets/pngperks/iconPerks_" + perk_name + ".png")): return True
    else: return False

# function to create a search bar for each perk
def create_perk_search_bar(self, perk_no, build_no, x, y):
    perk_search_bar = QtWidgets.QLineEdit(parent=self.centralwidget)
    perk_search_bar.setGeometry(QtCore.QRect(x, y, 130, 20))
    perk_search_bar.setObjectName("searchPerk_" + perk_no + "_Build_" + build_no) 
    # create completer for the search bar
    completer = list_of_all_perks()
    completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
    perk_search_bar.setCompleter(completer)
    perk_search_bar.textChanged.connect(lambda: on_selection_changed(self, perk_search_bar))
    return perk_search_bar

# function to create a custom button
def create_button(self, x, y, width, height, text):
    button = QtWidgets.QPushButton(parent=self.centralwidget)
    button.setGeometry(QtCore.QRect(x, y, width, height))
    font = QtGui.QFont()
    font.setFamily("Roboto")
    font.setPointSize(16)
    button.setFont(font)
    button.setObjectName("btn_" + text)
    button.setText(text)
    return button

# function to reset all perk search bars, this will in turn reset all the perk icons
def reset_perks(self):
    response = show_are_you_sure_popup()
    
    if response == QMessageBox.StandardButton.Yes:
        for i in range(1, 5):
            for j in range(1, 5): 
                line_edit = self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_" + str(j) + "_Build_" + str(i))
                line_edit.clear()

                perk_bg = self.centralwidget.findChild(QtWidgets.QLabel, "lblPerkBG_" + str(j) + "_Build_" + str(i))
                perk_bg.setPixmap(QtGui.QPixmap("assets/perks/perkBG.png"))

# function to format perk name into valid path to locate the perk icon
def format_perk_name(input_string):
    # Remove : ' - and extra spaces from the string
    formatted_string = input_string.replace(":", "").replace("'", "").replace("-", "").replace(" ", "")
    # Capitalize each word individually
    formatted_string = " ".join(word.capitalize() for word in formatted_string.split())
    return formatted_string

def open_settings_window(self):
    settings_window = Ui_SettingsWindow(self)
    settings_window.exec()  # Show the settings window modally

# function to return a QCompleter object with a list of all survivor perks
def list_of_all_perks():
    return QCompleter([
        'Ace in the Hole',
        'Adrenaline',
        'Aftercare',
        'Alert',
        'Any Means Necessary',
        'Appraisal',
        'Autodidact',
        'Babysitter',
        'Background Player',
        'Balanced Landing',
        'Bardic Inspiration',
        'Better Together',
        'Better Than New',
        'Bite the Bullet',
        'Blast Mine',
        'Blood Pact',
        'Blood Rush',
        'Boil Over',
        'Bond',
        'Boon: Circle of Healing',
        'Boon: Dark Theory',
        'Boon: Exponential',
        'Boon: Illumination',
        'Boon: Shadow Step',
        'Borrowed Time',
        'Botany Knowledge',
        'Breakdown',
        'Breakout',
        'Buckle Up',
        'Built to Last',
        'Calm Spirit',
        'Camaraderie',
        'Champion of Light',
        'Chemical Trap',
        'Clairvoyance',
        'Corrective Action',
        'Counterforce',
        'Cut Loose',
        'Dance With Me',
        'Dark Sense',
        'Dead Hard',
        'Deadline',
        'Deception',
        'Decisive Strike',
        'Deja Vu',
        'Deliverance',
        'Desperate Measures',
        'Detective\'s Hunch',
        'Distortion',
        'Diversion',
        'Dramaturgy',
        'Empathic Connection',
        'Empathy',
        'Fast Track',
        'Finesse',
        'Fixated',
        'Flashbang',
        'Flip-Flop',
        'Fogwise',
        'For the People',
        'Friendly Competition',
        'Hardened',
        'Head On',
        'Hope',
        'Hyperfocus',
        'Inner Focus',
        'Inner Strength',
        'Invocation: Weaving Spiders',
        'Iron Will',
        'Kindred',
        'Leader',
        'Left Behind',
        'Light-Footed',
        'Lightweight',
        'Lithe',
        'Low Profile',
        'Lucky Break',
        'Lucky Star',
        'Made For This',
        'Mettle of Man',
        'Mirrored Illusion',
        'No Mither',
        'No One Left Behind',
        'Object of Obsession',
        'Off the Record',
        'Open-Handed',
        'Overcome',
        'Overzealous',
        'Parental Guidance',
        'Pharmacy',
        'Plot Twist',
        'Plunderer\'s Instinct',
        'Poised',
        'Potential Energy',
        'Power Struggle',
        'Premonition',
        'Prove Thyself',
        'Quick and Quiet',
        'Quick Gambit',
        'Reactive Healing',
        'Reassurance',
        'Red Herring',
        'Repressed Alliance',
        'Residual Manifest',
        'Resilience',
        'Resurgence',
        'Rookie Spirit',
        'Saboteur',
        'Scavenger',
        'Scene Partner',
        'Second Wind',
        'Self-Care',
        'Self-Preservation',
        'Slippery Meat',
        'Small Game',
        'Smash Hit',
        'Sole Survivor',
        'Solidarity',
        'Soul Guard',
        'Specialist',
        'Spine Chill',
        'Sprint Burst',
        'Stake Out',
        'Still Sight',
        'Streetwise',
        'Strength in Shadows',
        'Teamwork: Collective Stealth',
        'Teamwork: Power of Two',
        'Technician',
        'Tenacity',
        'This is Not Happening',
        'Troubleshooter',
        'Unbreakable',
        'Up the Ante',
        'Urban Evasion',
        'Vigil',
        'Visionary',
        'Wake Up!',
        'We\'ll Make It',
        'We\'re Gonna Live Forever',
        'Wicked',
        'Windows of Opportunity',
        'Wiretap',
        # Castlevania Chapter
        'Eyes of Belmont',
        'Exultation',
        'Moment of Glory'
    ])

# main function
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
