import os
import socket
import tkinter
import json

from PySide6 import QtWidgets

SIZE = 1024
FORMAT = 'utf-8'
SEPERATOR = "@"


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
        print(data)
        cmd, msg = data.split(SEPERATOR)

        if cmd != "200":
            QtWidgets.QMessageBox.information(self.parent, "User exists", "User already exists. Please login.")

        self.login(username, password)

    def login(self, username, password):
        self.client.send(f"LOGIN{SEPERATOR}{username}{SEPERATOR}{password}".encode(FORMAT))

        data = self.client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split(SEPERATOR)

        if cmd == "FAILED":
            print("Failed to authenticate user. Goodbye.")
        else:
            QtWidgets.QMessageBox.information(self.parent, "Success", "You are now logged in")
            self.authenticated = True

    def upload(self):
        client_path = r""  # get users path
        ext = client_path.split('.')

        server_dir = "root"  # dir to store file

        if len(ext) < 2:
            # error
            pass
        else:
            file_size = os.path.getsize(client_path)
            file_name = client_path.split("\\")[-1]
            self.client.send(f"UPLOAD{SEPERATOR}{server_dir}{SEPERATOR}{file_name}".encode(FORMAT))  # send path to file

            data = self.client.recv(SIZE).decode(FORMAT)
            send_file = True
            if data == "OVERWRITE":  # prompt if they want to overwrite
                print("overwrite")
                # if yes then:
                self.client.send("YES".encode(FORMAT))
                send_file = True
                # else
                # self.client.send("NO".encode(FORMAT))
                # send_file = False

            if send_file:
                file = open(client_path, 'rb')
                # bytes_sent = SIZE
                data = file.read(SIZE)
                self.client.send(data)
                while data and self.client.recv(SIZE).decode(FORMAT) == "OK":
                    data = file.read(SIZE)
                    self.client.send(data)
                self.client.send("DONE".encode(FORMAT))
                print("Server received file")
                file.close()

    def download(self):
        server_path = r""  # path to file in server
        self.client.send(f"DOWNLOAD{SEPERATOR}{server_path}".encode(FORMAT))
        response = self.client.recv(SIZE).decode(FORMAT)
        if response == "OK":
            client_path = r"C:\Users\morbi\Downloads"
            nfile = open(client_path + "\\" + os.path.basename(server_path), "wb")
            data = self.client.recv(SIZE)  # after receive send conf
            self.client.send("OK".encode(FORMAT))

            while data != "DONE".encode(FORMAT):
                nfile.write(data)
                data = self.client.recv(SIZE)
                self.client.send("OK".encode(FORMAT))
            nfile.close()
            print("file received")

    def delete_file(self):
        server_path = ""
        self.client.send(f"DELETE{SEPERATOR}{server_path}".encode(FORMAT))
        response = self.client.recv(SIZE).decode(FORMAT)
        if response == "OK":
            print("File deleted from server.")
        else:
            print("File could not be removed.")

    def create_subfolder(self, subfolder_name, path):
        self.client.send(f"CREATE_SUBFOLDER{SEPERATOR}{path}{SEPERATOR}{subfolder_name}".encode(FORMAT))
        response = self.client.recv(SIZE).decode(FORMAT)
        if response == "CREATED":
            print("Subfolder created successfully.")
        else:
            print("Subfolder could not be created. Path does not exist.")

    def delete_subfolder(self, path_to_delete):
        self.client.send(f"DELETE{SEPERATOR}{path_to_delete}".encode(FORMAT))
        response = self.client.recv(SIZE).decode(FORMAT)
        if response == "OK":
            print("Subfolder deleted successfully.")
        else:
            print("Subfolder could not be deleted.")

    def list_all_files(self, path):
        self.client.send(f"LIST_DIRECTORY{SEPERATOR}{path}".encode(FORMAT))
        response = self.client.recv(SIZE).decode(FORMAT)
        if response == "OK":
            print("All files listed successfully.")
        else:
            print("Files could not all be listed.")


"""    while authenticated:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split('@')
        if cmd == "OK":
            print(f"{msg}")
        elif cmd == "DISCONNECTED":
            print(f"{msg}")
            break

        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "TASK":
            client.send(cmd.encode(FORMAT))
        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break

    print("Disconnected from the server. ")
    client.close()"""
