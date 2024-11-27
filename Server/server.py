import os
import socket
import threading
import sqlite3
import os
import hashlib


IP = "localhost"
PORT = 4450
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = 'utf-8'
SERVER_PATH = "server"
SEPERATOR = "@"


def handle_client(conn, addr):
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


def check_user(conn, addr):
    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]

        if cmd == "SIGNUP":
            username = data[1]
            password = data[2]
            print(f"Username: {username}")
            print(f"Password: {password}")

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
                send_data = "200@OK"
                conn.send(send_data.encode(FORMAT))
            else:
                send_data = "403@FORBIDDEN"
                conn.send(send_data.encode(FORMAT))
        elif cmd == "LOGIN":
            username = data[1]
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
        elif cmd == "UPLOAD":
            write_file = False
            if not os.path.isfile(data[1]):  # see if file already exists
                write_file = True
                conn.send("GOOD".encode(FORMAT))
            else:  # if file exists then check if they want to overwrite
                conn.send("OVERWRITE".encode(FORMAT))
                response = conn.recv(SIZE).decode(FORMAT)
                if response == "YES":
                    write_file = True
                else:
                    write_file = False

            if write_file:  # create the new file and store data
                nfile = open(data[1], "wb")
                data = conn.recv(SIZE)  # after receive send conf
                conn.send("OK".encode(FORMAT))

                while data != "DONE".encode(FORMAT):
                    nfile.write(data)
                    data = conn.recv(SIZE)
                    conn.send("OK".encode(FORMAT))
                nfile.close()
                print("file received")
        elif cmd == "DOWNLOAD":
            path = data[1]  # receive path
            send_data = True
            if os.path.isfile(path):  # see if file exists in server
                conn.send("OK".encode(FORMAT))  # let client know file has been found
            else:
                conn.send("NO".encode(FORMAT))
                send_data = False

            if send_data:
                file = open(path, 'rb')
                # bytes_sent = SIZE
                data = file.read(SIZE)
                conn.send(data)
                while data and conn.recv(SIZE).decode(FORMAT) == "OK":
                    data = file.read(SIZE)
                    conn.send(data)
                conn.send("DONE".encode(FORMAT))
                print("Server received file")
                file.close()
        elif cmd == "DELETE":
            server_path = data[1]  # path to file that is to be deleted
            if os.path.isfile(server_path):
                os.remove(server_path)
                conn.send("OK".encode(FORMAT))
            else:
                conn.send("NO".encode(FORMAT))
        elif cmd == "CREATE_SUBFOLDER":
            path = data[1]  # path passed in
            subfolder_name = data[2]  # subfolder name passed in
            path_to_create = os.path.join(path, subfolder_name)
            if os.path.exists(path_to_create):
                os.makedirs(path_to_create)
                conn.send("CREATED".encode(FORMAT))
            else:
                conn.send("NO".encode(FORMAT))

        elif cmd == "DELETE_SUBFOLDER":
            path_to_delete = data[1]
            if os.path.exists(path_to_delete):  # Checks if path to be deleted exists
                os.rmdir(path_to_delete)
                conn.send("DELETED".encode(FORMAT))
            else:
                conn.send("NO".encode(FORMAT))
        elif cmd == "LIST_DIR":

            # Helper function
            # Recursive function to list all files in directory then calls the function for every other directory
            def list_files_and_directories(path, indent):
                try:
                    # Gets all files and directories
                    items = os.listdir(path)

                    # Split files and directories into two different arrays
                    files = [item for item in items if os.path.isfile(os.path.join(path, item))]
                    directories = [item for item in items if os.path.isdir(os.path.join(path, item))]

                    print(f"{indent} Directory: {path}")
                    if files:
                        for file in files:
                            print(f"{indent} -{file}")
                    else:
                        print(f"{indent} No Files")

                    for directory in directories:
                        next_path = os.path.join(path, directory)
                        list_files_and_directories(next_path, indent + " ")

                except Exception as e:
                    print(f"There was an error in listing the files in the path {path}: {e}")
                    conn.send("NO".encode(FORMAT))

            root_directory = "root"
            list_files_and_directories(root_directory, "")
            conn.send("OK".encode(FORMAT))



def main():
    print("Starting the server...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"Server listening on {IP}: {PORT}")

    with sqlite3.connect("database.db") as db:
        my_cursor = db.cursor()
        sql = "PRAGMA table_info(users);"
        my_cursor.execute(sql)
        users = my_cursor.fetchone()
        print(users)
        if users is None:
            sql = """CREATE TABLE users (
                username varchar(255),
                password varchar(255)
            );"""
            my_cursor.execute(sql)
        db.commit()
        my_cursor.close()
    if not os.path.isdir("root"):
        os.mkdir("root")
        print("root directory created")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=check_user, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()
