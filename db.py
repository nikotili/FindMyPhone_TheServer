import pymysql as sql
import socket
import threading
from constants import *


def get_db_connection():
    return sql.connect(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME)


def insert_into_users(values):
    db = get_db_connection()
    cursor = db.cursor()
    query = "insert into users (%s) values (%s)" %(SIGN_UP_COLUMNS, values)
    cursor.execute(query)
    cursor.execute("select * from users")
    print(cursor.fetchone())
    print(cursor.fetchone())
    print(cursor.fetchone())
    db.commit()
    db.close()


def validate_sign_in(credentials):
    email, password = credentials.split(", ", 1)
    db = get_db_connection()
    cursor = db.cursor()
    query = "select Password from users where Email = %s" % email

    password = password.replace("'", "")

    cursor.execute(query)
    result = cursor.fetchone()
    result = str(result)
    result = result.replace("(", "").replace("'", "").replace(",", "").replace(")", "").replace(" ", "")

    if result == "None":
        return EMAIL_NOT_EXISTS_MESSAGE

    elif result == password:
        return SIGN_IN_SUCCESS_MESSAGE

    else:
        return WRONG_PASSWORD_MESSAGE


def handle_client(client_socket):
    received_request = client_socket.recv(DEFAULT_BUFFER_SIZE).decode()

    if SIGN_UP_REQUEST in received_request:
        try:
            received_request = received_request.replace(SIGN_UP_REQUEST, "")
            insert_into_users(received_request)
            client_socket.send(SIGN_UP_SUCCESS_MESSAGE.encode())
        except sql.err.IntegrityError:
            client_socket.send(EMAIL_IS_USED_ERROR_MESSAGE.encode())

    if SIGN_IN_REQUEST in received_request:
        try:
            received_request = received_request.replace(SIGN_IN_REQUEST, "")
            client_socket.send(validate_sign_in(received_request).encode())

        except:
            client_socket.send(GENERAL_ERROR_MESSAGE.encode())

    client_socket.close()


srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

srv_socket.bind((SRV_IP, SRV_PORT_DB))

srv_socket.listen(4)

while True:
    client, address = srv_socket.accept()
    client_handler = threading.Thread(handle_client(client))
    client_handler.start()
