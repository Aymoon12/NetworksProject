from PySide6 import QtWidgets, QtGui
from UI.LogIn import *

class LogIn(QtWidgets.QWidget, Ui_LogIn):
    def __init__(self, connector):
        super().__init__()
        self.setupUi(self)
        self.connector = connector
        self.pushButton.clicked.connect(self.login)
    
    def login(self):
        username = self.lineEdit_username.text().strip()
        password = self.lineEdit_password.text().strip()
        self.connector.login(username, password)