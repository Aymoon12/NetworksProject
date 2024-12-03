import os
import socket
import threading
import sqlite3
import os
import hashlib
import json
from Network_Analytics import *

IP = "localhost"
PORT = 4450
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = 'utf-8'
SERVER_PATH = "server"
SEPERATOR = "@"
BASE_PATH = "root"

session = threading.local()


def handle_client(conn, addr):  # handles client connections
    print(f"New connection from {addr}")
    conn.send("OK@Welcome to the server".encode(FORMAT))

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]

        send_data = "OK@"

        if cmd == "LOGOUT":
            break
        elif cmd == "TASK":
            send_data += "LOGOUT from the server.\n"
            conn.send(send_data.encode(FORMAT))

    print(f"{addr} disconnected")
    conn.close()


def check_valid_path(
        path):  # mainly checks to prevent someone  trying to gather information about folders outside their user's folder
    return path.startswith("\\") or path.startswith("/") or ".." in path or ":\\" in path


def check_valid_file_name(name):
    forbiddenchars = "/<>:\"/\\|?*"
    return any(elem in name for elem in forbiddenchars) or check_valid_path(name)


def check_user(conn, addr):  # controls what action the client performs
    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]

        match cmd:
            case "SIGNUP":  # creates a new user and stores it in the database
                username = data[1].lower()
                password = data[2]
                print(f"Username: {username}")
                print(f"Password: {password}")

                if (check_valid_file_name(username)):
                    send_data = "400@BAD_REQUEST"
                    conn.send(send_data.encode(FORMAT))
                    continue

                check_user = "SELECT * FROM users WHERE username = ?"
                val = (username,)

                result = None
                with sqlite3.connect("database.db") as db:
                    my_cursor = db.cursor()
                    my_cursor.execute(check_user, val)

                    result = my_cursor.fetchall()
                    my_cursor.close()
                print(result)
                if len(result) == 0:
                    with sqlite3.connect("database.db") as db:
                        my_cursor = db.cursor()
                        sql = "INSERT INTO users (username, password) VALUES (?, ?)"
                        val = (username, hashlib.sha256(password.encode(FORMAT)).hexdigest())
                        my_cursor.execute(sql, val)
                        db.commit()
                        my_cursor.close()
                    os.makedirs(os.path.join(BASE_PATH, username).replace("\\","/"))
                    send_data = "200@OK"
                    conn.send(send_data.encode(FORMAT))
                else:
                    send_data = "403@FORBIDDEN"
                    conn.send(send_data.encode(FORMAT))
            case "LOGIN":
                username = data[1].lower()
                password = data[2]

                sql = "SELECT * FROM users WHERE username = ? AND password =?"

                val = (username, hashlib.sha256(password.encode(FORMAT)).hexdigest())
                result = None
                with sqlite3.connect("database.db") as db:
                    my_cursor = db.cursor()
                    my_cursor.execute(sql, val)

                    result = my_cursor.fetchall()
                    my_cursor.close()

                print(result)
                if len(result) == 0:
                    send_data = "FAILED"
                    conn.send(f"{send_data}{SEPERATOR}{username}".encode(FORMAT))
                else:
                    send_data = "SUCCESS"
                    conn.send(f"{send_data}{SEPERATOR}{username}".encode(FORMAT))
                    session.username = username
            case "UPLOAD":

                if (session.username is None):
                    send_data = "UNAUTHORIZED"
                    conn.send(send_data.encode(FORMAT))
                    continue

                file_path = data[1]
                if (check_valid_path(file_path)):
                    send_data = "INVALID_FILE_PATH"
                    conn.send(send_data.encode(FORMAT))
                    continue

                file_name = data[2]
                if (check_valid_file_name(file_name)):
                    send_data = "INVALID_FILE_NAME"
                    conn.send(send_data.encode(FORMAT))
                    continue

                full_path = os.path.join(BASE_PATH, session.username, file_path, file_name).replace("\\","/")

                write_file = False
                if not os.path.isfile(full_path):  # see if file already exists
                    write_file = True
                    conn.send("GOOD".encode(FORMAT))
                else:  # if file exists then check if they want to overwrite
                    conn.send("OVERWRITE".encode(FORMAT))
                    response = conn.recv(SIZE).decode(FORMAT)
                    if response == "YES":
                        write_file = True
                    else:
                        write_file = False

                if write_file:
                    start_time = time.time()  # create the new file and store data
                    with open(full_path, "wb") as nfile:
                        data = conn.recv(SIZE)  # after receive send conf
                        conn.send("OK".encode(FORMAT))

                        while data != "DONE".encode(FORMAT):
                            nfile.write(data)
                            data = conn.recv(SIZE)
                            conn.send("OK".encode(FORMAT))

                    end_time = time.time()
                    file_size = os.path.getsize(full_path) * (1e-6)
                    transfer_time = end_time - start_time
                    upload_rate = file_size / transfer_time
                    system_response_time = end_time - start_time
                    save_upload_stats(session.username, file_name, file_size, upload_rate, transfer_time,
                                      system_response_time)

                    print("file received")
            case "DOWNLOAD":
                if (session.username is None):
                    send_data = "UNAUTHORIZED"
                    conn.send(send_data.encode(FORMAT))
                    continue
                path = data[1]
                if (check_valid_path(path)):
                    send_data = "INVALID_FILE_PATH"
                    conn.send(send_data.encode(FORMAT))
                    continue

                full_path = os.path.join(BASE_PATH, session.username, path).replace("\\","/")
                send_data = True
                if os.path.isfile(full_path):  # see if file exists in server
                    file_size = os.path.getsize(full_path)
                    conn.send(f"OK{SEPERATOR}{file_size}".encode(FORMAT))  # let client know file has been found
                    start_time = time.time()
                else:
                    conn.send("NO".encode(FORMAT))
                    send_data = False

                if send_data:
                    with open(full_path, 'rb') as file:
                        data = file.read(SIZE)
                        conn.send(data)
                        while data and conn.recv(SIZE).decode(FORMAT) == "OK":
                            data = file.read(SIZE)
                            conn.send(data)

                        conn.send("DONE".encode(FORMAT))

                        end_time = time.time()
                        transfer_time = end_time - start_time
                        download_rate = file_size * (1e-6) / transfer_time
                        system_response_time = end_time - start_time  # Simplified for now
                        save_download_stats(session.username, os.path.basename(full_path), file_size * (1e-6),
                                            download_rate,
                                            transfer_time, system_response_time)
                        print("Server received file")

            case "DELETE":  # deletes a file
                if (session.username is None):
                    send_data = "UNAUTHORIZED"
                    print("test2")
                    conn.send(send_data.encode(FORMAT))
                    continue
                server_path = data[1]
                if (check_valid_path(path)):
                    send_data = "INVALID_FILE_PATH"
                    print("test1")
                    conn.send(send_data.encode(FORMAT))
                    continue

                full_path = os.path.join(BASE_PATH, session.username, server_path).replace("\\","/")

                try:
                    if os.path.isfile(full_path):
                        os.remove(full_path)
                        conn.send("OK".encode(FORMAT))
                        continue
                    if os.path.isdir(full_path):
                        os.rmdir(full_path)
                        conn.send("OK".encode(FORMAT))
                        continue
                    raise OSError
                except OSError as ose:
                    print("test3")
                    print(full_path)
                    conn.send("NO".encode(FORMAT))
                    print(ose)
            case "CREATE_SUBFOLDER":  # creates a subfolder
                if (session.username is None):
                    send_data = "UNAUTHORIZED"
                    conn.send(send_data.encode(FORMAT))
                    continue
                path = data[1]
                subfolder_name = data[2]
                if (check_valid_path(path) or check_valid_file_name(subfolder_name)):
                    send_data = "INVALID_FILE_PATH"
                    conn.send(send_data.encode(FORMAT))
                    continue
                path_to_create = os.path.join(BASE_PATH, session.username, path, subfolder_name).replace("\\","/")
                try:
                    os.makedirs(path_to_create)
                    conn.send("CREATED".encode(FORMAT))
                except OSError:
                    conn.send("NO".encode(FORMAT))

            case "LIST_DIR":  # lets users view files in current directory
                if (session.username is None):
                    send_data = "UNAUTHORIZED"
                    conn.send(send_data.encode(FORMAT))
                    continue

                path = data[1]
                if (check_valid_path(path)):
                    send_data = "INVALID_FILE_PATH"
                    conn.send(send_data.encode(FORMAT))
                    continue

                full_path = os.path.join(BASE_PATH, session.username, path).replace("\\","/")
                json_dict = None
                try:
                    # Gets all files and directories
                    items = os.listdir(full_path)

                    # Split files and directories into two different arrays
                    files = [item for item in items if os.path.isfile(os.path.join(full_path, item).replace("\\","/"))]
                    directories = [item for item in items if os.path.isdir(os.path.join(full_path, item).replace("\\","/"))]

                    json_dict = json.dumps({"Files": files, "Directories": directories}).encode(FORMAT)

                except Exception as e:
                    print(f"There was an error in listing the files in the path {full_path}: {e}")
                    conn.send("NO".encode(FORMAT))
                    continue

                conn.send("OK".encode(FORMAT))
                for data in [json_dict[i:i + SIZE] for i in range(0, len(json_dict),
                                                                  SIZE)]:  # incase you have an unreasonably long folder with files and subfolders with lengths longer than 1024 bytes
                    resp = conn.recv(SIZE).decode(FORMAT)
                    if resp != "OK":
                        break
                    conn.send(data)
                conn.send("DONE".encode(FORMAT))


def main():
    print("Starting the server...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.gethostname(), PORT))
    server.listen()
    print(f"Server listening on {IP}: {PORT}")

    with sqlite3.connect("database.db") as db:
        my_cursor = db.cursor()
        sql = "PRAGMA table_info(users);"
        my_cursor.execute(sql)
        users = my_cursor.fetchone()
        print(users)
        if users is None:  # create the user table if it doesnt exist
            sql = """CREATE TABLE users (
                username varchar(255),
                password varchar(255)
            );"""
            my_cursor.execute(sql)
        db.commit()
        my_cursor.close()
    if not os.path.isdir("root"):  # create root is it doesnt exist
        os.mkdir("root")
        print("root directory created")

    network_analytics_init()  # begin network analysis
    while True:  # start the server
        conn, addr = server.accept()
        thread = threading.Thread(target=check_user, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()
