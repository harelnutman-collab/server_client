import socket
from PIL import Image
import os


def recv_image_data(client_socket, file_name, file_data_len):
    """
    receive the image data and save the image
    :param client_socket: the client socket
    :param file_name:  the image file name
    :param file_data_len: the length of the image data
    :return:None
    """

    data = b''
    while len(data) < file_data_len:
        slice = file_data_len - len(data)
        if slice > 1024:
            data += client_socket.recv(1024)
        else:
            data += client_socket.recv(slice)
            break

    # create the image file
    with open (file_name, "wb") as f:
        f.write(data)


my_sock = socket.socket()


try:
    my_sock.connect(("127.0.0.1", 1455))

except Exception as e:
    my_sock.close()
    exit(f"server is down - try again {str(e)}")



while True:
    msg = input("enter msg to send or exit to finish ")
    if msg.lower() == "exit":
        break



    if msg.lower() == "screenshot":
        try:
            my_sock.send(msg.encode())

            file_name_len = int(my_sock.recv(2).decode())
            file_name = my_sock.recv(file_name_len).decode()
            file_data_len = int(my_sock.recv(6).decode())
            recv_image_data(my_sock, file_name, file_data_len)

            im = Image.open("screenshot.jpg")
            im.show()



        except Exception as e:
            print(f"error in receive or sending data {str(e)}")


my_sock.close()
print("bye bye")







