import os
import socket
import threading
import mysql.connector
import os
import hashlib

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("MYSQL_PASSWORD"),
    database="filesharingsystem"
)

my_cursor = db.cursor()

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

        check_user = "SELECT * FROM users WHERE username = %s"
        val = (username,)

        my_cursor.execute(check_user,val)

        result = my_cursor.fetchall()
        print(result)
        if len(result) == 0:
            sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
            val = (username, hashlib.sha256(password.encode(FORMAT)).hexdigest())
            my_cursor.execute(sql, val)
            db.commit()
        else:
            send_data = "403"
            conn.send(send_data.encode(FORMAT))
    elif cmd == "LOGIN":
        username = data[1]
        password = data[2]

        sql = "SELECT * FROM users WHERE username = %s AND password =%s"

        val = (username, hashlib.sha256(password.encode(FORMAT)).hexdigest())
        my_cursor.execute(sql, val)

        result = my_cursor.fetchall()
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
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=check_user, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    print(db)
    main()
