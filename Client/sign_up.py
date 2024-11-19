from PySide6 import QtWidgets, QtGui
from UI.SignUp import *

class SignUp(QtWidgets.QWidget, Ui_SignUp):
    def __init__(self, connector):
        super().__init__()
        self.setupUi(self)
        self.connector = connector
        self.pushButton.clicked.connect(self.signup)
    
    def signup(self):
        if(self.lineEdit_password.text().strip() != self.lineEdit_confirm.text().strip()):
            print("Passwords dont match")
        else:
            username = self.lineEdit_username.text().strip()
            password = self.lineEdit_password.text().strip()
            self.connector.signup(username, password)