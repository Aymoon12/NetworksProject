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
            my_cursor.execute(check_user,val)

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

        my_cursor.execute(sql)
        db.commit()
        my_cursor.close()


    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=check_user, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()
