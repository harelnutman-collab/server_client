import socket
from PIL import Image
import os


def send_data(client, data_len_byte, data):
    if tyep(data) == str:
        data = data.encode()
    try:
      client.send(str(len(data)).zfill(data_len_byte).encode())
      client.send(data)
    except Exception as e:
        print(f"error in recv/send try again {str(e)}")

def recv_image_data(client_socket, file_data_len):
    """
    receive the image data and save the image
    :param client_socket: the client socket
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
    with open ("screenshot.jpg", "wb") as f:
        f.write(data)

    im = Image.open("screenshot.jpg")
    im.show()

func_tuple_client = ("screenshot", "open process")
my_sock = socket.socket()


try:
    my_sock.connect(("127.0.0.1", 1452  ))

except Exception as e:
    my_sock.close()
    exit(f"server is down - try again {str(e)}")

menu = "choose:\n 1 = screenshott\n 2 = copy\n 9 - exit\n enter your choice: "

while True:
    msg = input(menu)
    if msg == '9':
        break

    elif msg.lower() not in ['1', '2']:
        print("not valid input")
        continue

    else:
        try:
            my_sock.send(msg.encode())
        except Exception as e:
            print(f"error in receive or sending data {str(e)}")

        if msg == "1": # screen shoot
            try:
                file_data_len = int(my_sock.recv(6).decode())
                recv_image_data(my_sock, file_data_len)
            except Exception as e:
                print(f"error in receive or sending data {str(e)}")
                break



        elif msg.lower() == "2":
            msg = input("enter the name of the process")
            send_data(my_sock, 2, msg)

my_sock.close()
print("bye bye")







