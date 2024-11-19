from PySide6 import QtWidgets, QtGui
from UI.ConnectToServer import *

class ConnectToServer(QtWidgets.QWidget, Ui_ConnectToServer):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.pushButton.clicked.connect(self.connect)
    
    def connect(self):
        ip = self.lineEdit_IP.text().strip()
        port = self.lineEdit_port.text().strip()
        self.parent.connect(ip, port)