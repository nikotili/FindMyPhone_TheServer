import socket
import threading
from constants import *

flag = True
image_index = 1


def receive_file_from(client_socket):
    global image_index
    header = client_socket.recv(DEFAULT_BUFFER_SIZE)
    if IMAGE.encode() == header:
        received_bytes = client_socket.recv(DEFAULT_BUFFER_SIZE)

        file = open(get_image_name(image_index), "ab")

        while received_bytes != ''.encode():
            file.write(received_bytes)
            received_bytes = client_socket.recv(DEFAULT_BUFFER_SIZE)
        file.close()
        client_socket.close()

    elif PHP_SIGNATURE.encode() in header:
        print("sending to php index: " + str(image_index))
        client_socket.send(get_image_name(image_index).encode())
        image_index += 1

    # elif AUDIO.encode() == header:
    #     received_bytes = client_socket.recv(MAX_BUFFER_SIZE)
    #     file = open("test.mp3", "ab")
    #     file.write(received_bytes)
    #     file.close()
    #


def get_image_name(index):
    return "image-" + str(index) + ".jpg"


srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

srv_socket.bind((SRV_IP, SRV_PORT_FILES))

srv_socket.listen(4)

while True:
    client, addr = srv_socket.accept()
    client_handler = threading.Thread(receive_file_from(client))
    client_handler.start()
