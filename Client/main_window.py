from UI.MainWindow import *
from networking import Connector
from connect_to_server import ConnectToServer
from sign_up import SignUp
from log_in import LogIn
from progress import Progress
from preferences import Preferences
from upload_folder import UploadFolder
from PySide6 import QtWidgets, QtGui, QtCore
import qdarktheme
import json
import os

class ListItem(QtWidgets.QListWidgetItem):
    def __init__(self, name, listwidget, isdir):
        super().__init__(name, listwidget, isdir)
        self.isDirectory = isdir

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        try:
            with open("settings.json", "r+") as infile:
                self.settings = json.load(infile)
                if(self.settings["theme"] == "dark"):
                    self.actionUploadFile.setIcon(QtGui.QIcon("Icons/upload-dark-mode.svg"))
                    self.actionCreateSubfolder.setIcon(QtGui.QIcon("Icons/folder-plus-dark-mode.svg"))
                qdarktheme.setup_theme(self.settings["theme"])
        except FileNotFoundError:
            with open("settings.json", "w+") as infile: #default
                self.settings = {}
                self.settings["theme"] = "dark"
                self.actionUploadFile.setIcon(QtGui.QIcon("Icons/upload-dark-mode.svg"))
                self.actionCreateSubfolder.setIcon(QtGui.QIcon("Icons/folder-plus-dark-mode.svg"))
                qdarktheme.setup_theme("dark")
                infile.write(json.dumps(self.settings))
        
        self.connector = None
        self.ConnectionWindow = None
        self.SignUpWindow = None
        self.LoginWindow = None
        self.SettingsWindow = None
        self.ProgressWindow = None
        self.CreateFolderWindow = None
        self._curPath = ""
        self.actionSign_Up.triggered.connect(self.open_signup_window)
        self.actionLog_In.triggered.connect(self.open_login_window)
        self.actionConnect_to_Server.triggered.connect(self.open_connection_window)
        self.actionPreferences.triggered.connect(self.open_settings_window)
        self.actionUploadFile.triggered.connect(self.upload_file)
        self.actionCreateSubfolder.triggered.connect(self.open_create_folder_window)
        self.listWidget.itemDoubleClicked.connect(self.open_folder)
        self.listWidget.installEventFilter(self)
    
    def setListWidget(self, directory_list):
        self.listWidget.clear()
        iconProvider = QtWidgets.QFileIconProvider()
        if(self.get_path() != ""):
            directory_list["Directories"].insert(0, "..")
        for directory in directory_list["Directories"]:
            item = ListItem(directory, self.listWidget, True)
            item.setIcon(iconProvider.icon(iconProvider.IconType.Folder))
        for file in directory_list["Files"]:
            item = ListItem(file, self.listWidget, False)
            item.setIcon(iconProvider.icon(QtCore.QFileInfo(file)))

    def eventFilter(self, source, event):
        """
        Overrides the normal main window function to add the right-click context menu to each list item
        """
        if event.type() == QtCore.QEvent.ContextMenu and source is self.listWidget:
            menu = QtWidgets.QMenu()
            item = source.itemAt(event.pos())
            if(item.isDirectory):
                action = QAction(self)
                action.setText("Open Folder")
                action.triggered.connect(lambda: self.open_folder(item))
                menu.addAction(action)
                action = QAction(self)
                action.setText("Delete Folder")
                action.triggered.connect(lambda: self.delete_file(item))
                menu.addAction(action)
            else:
                action = QAction(self)
                action.setText("Download File")
                action.triggered.connect(lambda: self.download_file(item))
                menu.addAction(action)
                action = QAction(self)
                action.setText("Delete File")
                action.triggered.connect(lambda: self.delete_file(item))
                menu.addAction(action)

            menu.exec(event.globalPos())
            return True
        return super(MainWindow, self).eventFilter(source, event)


    def closeEvent(self, event):
        QtWidgets.QApplication.closeAllWindows()
        event.accept()

    def connect(self, ip, port):
        try:
            self.connector = Connector(self, ip, port)
        except ConnectionRefusedError:
            QtWidgets.QMessageBox.critical(self, "ERROR", "Connection Refused")
            self.connector = None
        except ValueError:
            QtWidgets.QMessageBox.critical(self, "ERROR", "Input a proper port number")
            self.connector = None
        else:
            self.actionSign_Up.setEnabled(True)
            self.actionLog_In.setEnabled(True)
            self.actionConnect_to_Server.setEnabled(False)
            self.ConnectionWindow.close()
            QtWidgets.QMessageBox.information(self, "Connection", "You are now connected to the server")
            
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
    
    def open_settings_window(self):
        self.SettingsWindow = Preferences(self)
        self.SettingsWindow.show()

    def open_progress_window(self, amount, type = "Uploading"):
        self.ProgressWindow = Progress(type, amount)
        self.ProgressWindow.show()

    def open_create_folder_window(self):
        self.CreateFolderWindow = UploadFolder(self)
        self.CreateFolderWindow.show()

    def save_settings(self):
        with open("settings.json", "w+") as infile:
            if(self.settings["theme"] == "dark"):
                self.actionUploadFile.setIcon(QtGui.QIcon("Icons/upload-dark-mode.svg"))
                self.actionCreateSubfolder.setIcon(QtGui.QIcon("Icons/folder-plus-dark-mode.svg"))
            else:
                self.actionUploadFile.setIcon(QtGui.QIcon("Icons/upload.svg"))
                self.actionCreateSubfolder.setIcon(QtGui.QIcon("Icons/folder-plus.svg"))
            qdarktheme.setup_theme(self.settings["theme"])
            infile.write(json.dumps(self.settings))
    
    def set_path(self, path):
        self._curPath = path
        self.setListWidget(json.loads(self.connector.list_all_files(path)))
        self.label.setText("Current Folder: " + path)
        if(path == ""):
            self.label.setText("Current Folder: root")

    def get_path(self):
        return self._curPath
    
    
    def open_folder(self, listitem):
        if(not listitem.isDirectory):
            self.download_file(listitem)
            return
        new_path = ""
        if(listitem.text() == ".."):
            new_path = os.path.dirname(self.get_path())
        else:
            new_path = os.path.join(self.get_path(),listitem.text())
        self.set_path(new_path)
    def download_file(self, listitem):
        directory = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Choose directory to download to", "", QtWidgets.QFileDialog.ShowDirsOnly))
        if directory != "":
            self.connector.download(directory, os.path.join(self.get_path(),listitem.text()))

    def delete_file(self, listitem):
        self.connector.delete_file(os.path.join(self.get_path(), listitem.text()))

    def upload_file(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName()
        if(file_path[0] != ""):
            self.connector.upload(file_path[0], self.get_path())

    def create_folder(self, folder_name):
        self.connector.create_subfolder(folder_name, self.get_path())
