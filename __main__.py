# server
import socket
import threading
from constants import *

i = 0
message_for_php = "".encode()
message_for_java = "".encode()


def handle_client(client_socket):
    global message_for_java
    global message_for_php
    global i
    received_bytes = client_socket.recv(MAX_BUFFER_SIZE)
    i += 1
    print(str(i) + ": " + received_bytes.decode())
    print("Message for phone:" + message_for_java.decode())
    # client_socket.send(PYTHON_SIGNATURE.encode())
    # client_socket.close()
    if PHP_SIGNATURE.encode() in received_bytes:
        message_for_java = received_bytes.replace(PHP_SIGNATURE.encode(), "".encode())
        if message_for_php != "".encode():
            print("Sending to web: " + message_for_php.decode())
            client_socket.send(message_for_php)
            message_for_php = "".encode()
            client_socket.close()

    if JAVA_SIGNATURE.encode() in received_bytes:
        message_for_php = received_bytes.replace(JAVA_SIGNATURE.encode(), "".encode())
        print("Message for web:" + message_for_php.decode())
        if message_for_java != "".encode():
            print("Sending to phone: " + message_for_java.decode())
            client_socket.send(message_for_java)
            message_for_java = "".encode()
            client_socket.close()

    print("################################################################")


srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

srv_socket.bind((SRV_IP, SRV_PORT))

srv_socket.listen(4)

while True:
    client, address = srv_socket.accept()
    client_handler = threading.Thread(handle_client(client))
    client_handler.start()
