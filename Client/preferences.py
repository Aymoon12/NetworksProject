from PySide6 import QtWidgets, QtGui
from UI.Preferences import *

class Preferences(QtWidgets.QWidget, Ui_Preferences):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.pushButtonSavePreferences.clicked.connect(self.save_preferences)
        if(parent.settings["theme"] == "dark"):
            self.checkBoxDarkMode.setChecked(True)
    
    def save_preferences(self):
        if(self.checkBoxDarkMode.isChecked()):
            self.parent.settings["theme"] = "dark"
        else:
            self.parent.settings["theme"] = "light"
        self.parent.save_settings()
        self.close()