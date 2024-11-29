import os
import socket
import json
import time

from PySide6 import QtWidgets, QtCore
qm = QtWidgets.QMessageBox

SIZE = 1024
FORMAT = 'utf-8'
SEPERATOR = "@"

def check_invalid_query(data):
    match data:
        case "UNAUTHORIZED":
            raise ValueError("Unauthorized Connection")
        case "INVALID_FILE_PATH":
            raise ValueError("Invalid File Path")
        case "INVALID_FILE_NAME":
            raise ValueError("Invalid File Name")

class Uploader(QtCore.QObject):
    finished = QtCore.Signal()
    progress = QtCore.Signal(int)
    def __init__(self, client, client_path):
        super().__init__()
        self.client = client
        self.client_path = client_path

    def run(self):
        with open(self.client_path, 'rb') as file:
            data = file.read(SIZE)
            self.client.send(data)
            kb_sent = 1
            self.progress.emit(kb_sent)
            timer = QtCore.QTimer()
            timer.timeout.connect(self, lambda: self.progress.emit(kb_sent))
            timer.start(100)
            while data and self.client.recv(SIZE).decode(FORMAT) == "OK":
                data = file.read(SIZE)
                self.client.send(data)
                kb_sent += 1
                QtCore.QCoreApplication.processEvents()
            self.client.send("DONE".encode(FORMAT))
            self.client.recv(SIZE) #since the server still replies OK one last time
        self.finished.emit()

class Downloader(QtCore.QObject):
    finished = QtCore.Signal()
    progress = QtCore.Signal(int)
    def __init__(self, client, local_path, server_path):
        super().__init__()
        self.client = client
        self.local_path = local_path
        self.server_path = server_path

    def run(self):
        with open(os.path.join(self.local_path, os.path.basename(self.server_path)), "wb") as nfile:
            data = self.client.recv(SIZE)  # after receive send conf
            self.client.send("OK".encode(FORMAT))

            kb_recvd = 1
            self.progress.emit(kb_recvd)
            curSec = time.time()

            while data != "DONE".encode(FORMAT):
                nfile.write(data)
                data = self.client.recv(SIZE)
                self.client.send("OK".encode(FORMAT))
                kb_recvd += 1
                if time.time() > curSec + 0.1:
                    curSec = time.time()
                    self.progress.emit(kb_recvd)
        self.finished.emit()

class Connector():
    def __init__(self, parent, ip, port):
        self.parent = parent
        self.addr = (ip, int(port))
        self.client = None
        self.authenticated = False
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.addr)

    def signup(self, username, password):

        self.client.send(f"SIGNUP{SEPERATOR}{username}{SEPERATOR}{password}".encode(FORMAT))
        data = self.client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split(SEPERATOR)

        if cmd != "200":
            qm.information(self.parent, "User exists", "User already exists. Please login.")

        self.login(username, password)

    def login(self, username, password):
        self.client.send(f"LOGIN{SEPERATOR}{username}{SEPERATOR}{password}".encode(FORMAT))

        data = self.client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split(SEPERATOR)

        if cmd == "FAILED":
            qm.critical(self.parent, "ERROR", "Failed to authenticate user.")
        else:
            qm.information(self.parent, "Success", "You are now logged in")
            self.authenticated = True
            self.parent.actionSign_Up.setEnabled(False)
            self.parent.actionLog_In.setEnabled(False)
            self.parent.actionUploadFile.setEnabled(True)
            self.parent.actionCreateSubfolder.setEnabled(True)
            self.parent.set_path(self.parent.get_path())

    def upload(self, client_path, server_dir):
        
        #ext = client_path.split('.')

        file_size = os.path.getsize(client_path)
        file_name = client_path.split("/")[-1]
        self.client.send(f"UPLOAD{SEPERATOR}{server_dir}{SEPERATOR}{file_name}".encode(FORMAT))  # send path to file

        data = self.client.recv(SIZE).decode(FORMAT)
        check_invalid_query(data)
        send_file = True
        if data == "OVERWRITE":  # prompt if they want to overwrite
            
            
            ret = qm.question(self.parent, 'Confirm', "A file already exists on the server at this path, do you want to overwrite it?", qm.Yes | qm.No)
            if ret == qm.Yes:
                self.client.send("YES".encode(FORMAT))
                send_file = True
            else:
                self.client.send("NO".encode(FORMAT))
                send_file = False
            


        if send_file:
            self.parent.open_progress_window(file_size)
            self.parent.setEnabled(False)
            self.thread = QtCore.QThread()
            self.worker = Uploader(self.client, client_path)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.finished.connect(self.parent.ProgressWindow.close)
            self.thread.finished.connect(lambda: self.parent.setEnabled(True))
            self.thread.finished.connect(lambda: self.parent.set_path(self.parent.get_path())) #resets the file list so the file is added in the file list
            self.worker.progress.connect(self.parent.ProgressWindow.setProgress)
            self.thread.start()
            

    def download(self, local_path, server_path):
        self.client.send(f"DOWNLOAD{SEPERATOR}{server_path}".encode(FORMAT))
        response = self.client.recv(SIZE).decode(FORMAT)
        check_invalid_query(response)
        if response.startswith("OK"):
            file_size = int(response.split('@')[1])
            self.parent.open_progress_window(file_size, "Downloading")
            self.parent.setEnabled(False)
            self.thread = QtCore.QThread()
            self.worker = Downloader(self.client, local_path, server_path)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.finished.connect(self.parent.ProgressWindow.close)
            self.thread.finished.connect(lambda: self.parent.setEnabled(True))
            self.worker.progress.connect(self.parent.ProgressWindow.setProgress)
            self.thread.start()

    def delete_file(self, server_path):
        self.client.send(f"DELETE{SEPERATOR}{server_path}".encode(FORMAT))
        response = self.client.recv(SIZE).decode(FORMAT)
        check_invalid_query(response)
        if response == "OK":
            self.parent.set_path(self.parent.get_path())
        else:
            qm.critical(self.parent, "ERROR", "File/Subfolder could not be deleted")

    def create_subfolder(self, subfolder_name, path):
        self.client.send(f"CREATE_SUBFOLDER{SEPERATOR}{path}{SEPERATOR}{subfolder_name}".encode(FORMAT))
        response = self.client.recv(SIZE).decode(FORMAT)
        check_invalid_query(response)
        if response == "CREATED":
            self.parent.set_path(self.parent.get_path())
        else:
            qm.critical(self.parent, "ERROR", "Subfolder could not be created")


    def list_all_files(self, path):
        self.client.send(f"LIST_DIR{SEPERATOR}{path}".encode(FORMAT))
        response = self.client.recv(SIZE).decode(FORMAT)
        check_invalid_query(response)
        if response == "OK":
            self.client.send("OK".encode(FORMAT))
            json = b''
            data = self.client.recv(SIZE)
            while(data != "DONE".encode(FORMAT)):
                json += data
                data = self.client.recv(SIZE)
                self.client.send("OK".encode(FORMAT))
            return json.decode(FORMAT)
        else:
            raise FileNotFoundError()



