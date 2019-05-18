import socket
import threading
from constants import *

flag = True


def receive_file_from(client_socket):

    header = client_socket.recv(DEFAULT_BUFFER_SIZE)
    if IMAGE.encode() == header:
        received_bytes = client_socket.recv(DEFAULT_BUFFER_SIZE)
        file = open("image.jpg", "ab")
        while received_bytes != ''.encode():
            file.write(received_bytes)
            received_bytes = client_socket.recv(DEFAULT_BUFFER_SIZE)
        file.close()

    # elif AUDIO.encode() == header:
    #     received_bytes = client_socket.recv(MAX_BUFFER_SIZE)
    #     file = open("test.mp3", "ab")
    #     file.write(received_bytes)
    #     file.close()
    #
    # elif TEXT.encode() == header:
    #     received_bytes = client_socket.recv(MAX_BUFFER_SIZE)
    #     file = open("test.txt", "ab")
    #     file.write(received_bytes)
    #     file.close()


srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

srv_socket.bind((SRV_IP, SRV_PORT_FILES))

srv_socket.listen(4)

while True:
    client, addr = srv_socket.accept()
    client_handler = threading.Thread(receive_file_from(client))
    client_handler.start()
