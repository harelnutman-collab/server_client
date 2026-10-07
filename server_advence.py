import socket
from PIL import ImageGrab
import subprocess

server_sock = socket.socket()
server_sock.bind(("0.0.0.0", 1452))
server_sock.listen(3)
func_tuple = ("screenshot", "open process")

while True:
    #wait to clients

    client_sock, addr = server_sock.accept()

    print(f"{addr[0]} - connected")
    # handle the client
    while True:
        try:
            data = client_sock.recv(20).decode()
            if data.lower() not in func_tuple:
                break
            print(f"getting data - {data}")

            if data.lower() == "screenshot":
                im = ImageGrab.grab()
                im.save('screenshot.jpg')
                with open('screenshot.jpg', 'rb') as file:
                    image_data = file.read()
                file_data_len = str(len(image_data)).zfill(6)
                file_name = "screenshot.jpg"
                file_name_len = str(len(image_data)).zfill(2)

                try:
                    client_sock.send(file_name_len)
                    client_sock.send(file_name)
                    client_sock.send(file_data_len)
                    client_sock.sendall(image_data)

                except Exception as e:
                    print("")

            if data == "open process":
                try:
                    print("f")
                    subprocess.call(data)
                except Exception as e:
                    print(f"error in recv/send try again {str(e)}")

        except Exception as e:
            print(f"error in recv/send try again {str(e)}")
