from UI.MainWindow import *
from networking import Connector
from connect_to_server import ConnectToServer
from sign_up import SignUp
from log_in import LogIn
from PySide6 import QtWidgets, QtGui
import qdarktheme
import json


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        try:
            with open("settings.json", "r+") as infile:
                self.settings = json.load(infile) 
                qdarktheme.setup_theme(self.settings["theme"])
        except:
            with open("settings.json", "w+") as infile: #default
                self.settings = {}
                self.settings["theme"] = "dark"
                qdarktheme.setup_theme("dark")
                infile.write(json.dumps(self.settings))
        
        self.connector = None
        self.ConnectionWindow = None
        self.SignUpWindow = None
        self.LoginWindow = None
        self.actionSign_Up.triggered.connect(self.open_signup_window)
        self.actionLog_In.triggered.connect(self.open_login_window)
        self.actionConnect_to_Server.triggered.connect(self.open_connection_window)
    
    def connect(self, ip, port):
        try:
            self.connector = Connector(ip, port)
        except ConnectionRefusedError:
            print("Connection Refused") #will turn into exception windows in the future
            self.connector = None
        except ValueError:
            print("Input a proper port number")
            self.connector = None
    
    def open_connection_window(self):
        self.ConnectionWindow = ConnectToServer(self)
        self.ConnectionWindow.show()
    
    def open_signup_window(self):
        if(self.connector is not None):
            if(not self.connector.authenticated):
                self.SignUpWindow = SignUp(self.connector)
                self.SignUpWindow.show()

    def open_login_window(self):
        if(self.connector is not None):
            if(not self.connector.authenticated):
                self.LoginWindow = LogIn(self.connector)
                self.LoginWindow.show()