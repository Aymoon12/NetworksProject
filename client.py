import os
import socket

IP = "localhost"
PORT = 4450
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = 'utf-8'
SEPERATOR = "@"
SERVER_DATA_PATH = "server_data"


def main():
    authenticated = False
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    option = input("1. Sign up\n2. Login\n")
    if option == '1':
        username = input("username: ")
        password = input("password: ")

        client.send(f"SIGNUP{SEPERATOR}{username}{SEPERATOR}{password}".encode(FORMAT))
        data = client.recv(SIZE).decode(FORMAT)

        cmd, msg = data.split(SEPERATOR)

        if cmd == "200":
            print("Signed Up Successfully. Please Login.")
        else:
            print("User Already Exists. Please Login.")
        option = 2

    if option == '2':
        username = input("username: ")
        password = input("password: ")

        client.send(f"LOGIN{SEPERATOR}{username}{SEPERATOR}{password}".encode(FORMAT))

        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split(SEPERATOR)

        if cmd == "FAILED":
            print("Failed to authenticate user. Goodbye.")
        else:
            authenticated = True

    while authenticated:
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
    client.close()


if __name__ == "__main__":
    main()
