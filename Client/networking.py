import os
import socket

SIZE = 1024
FORMAT = 'utf-8'
SEPERATOR = "@"

class Connector():
    def __init__(self, ip, port):
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

        if cmd == "200":
            print("Signed Up Successfully. Please Login.") #will eventually make windows for these print statements
        else:
            print("User Already Exists. Please Login.")
        self.login(username, password)
    
    def login(self, username, password):
        self.client.send(f"LOGIN{SEPERATOR}{username}{SEPERATOR}{password}".encode(FORMAT))

        data = self.client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split(SEPERATOR)

        if cmd == "FAILED":
            print("Failed to authenticate user. Goodbye.")
        else:
            self.authenticated = True



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

