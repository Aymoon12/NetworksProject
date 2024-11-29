from PySide6 import QtWidgets, QtGui
from UI.Progress import *

class Progress(QtWidgets.QWidget, Ui_Progress):
    def __init__(self, type, amount):
        super().__init__()
        self.setupUi(self)
        self.labelType.setText(type)
        self.exp = 0
        while amount > 1024:
            amount /= 1024
            self.exp += 1
        self.progressBar.setMaximum(amount)

    def setProgress(self, progress):
        #self.progressBar.setValue(progress / (1024 ** self.exp))
        if(progress > 1024 * 1024 * 1024):
            self.labelKb.setText("%.2f" % (progress / (1024 * 1024 * 1024)) + " GB")
        elif progress > 1024 * 1024:
            self.labelKb.setText("%.2f" % (progress / (1024 * 1024)) + " MB")
        else:
            self.labelKb.setText("%.2f" % (progress / (1024 * 1024 * 1024)) + " KB")
        
        for _ in range(self.exp):
            progress /= 1024
        self.progressBar.setValue(progress)