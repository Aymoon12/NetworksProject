from PySide6 import QtWidgets
from UI.UploadFolder import *

class UploadFolder(QtWidgets.QWidget, Ui_UploadFolder):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.pushButtonUpload.clicked.connect(self.createfolder)
    
    def createfolder(self):
        folder_name = self.lineEditFolderName.text().strip()
        self.parent.create_folder(folder_name)
        self.close()