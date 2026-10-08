import socket
from PIL import ImageGrab
import subprocess

server_sock = socket.socket()
server_sock.bind(("0.0.0.0", 1452))
server_sock.listen(3)


def send_data(client, data_len_byte, data):
    if tyep(data) == str:
        data = data.encode()
    try:
      client.send(str(len(data)).zfill(data_len_byte).encode())
      client.send(data)
    except Exception as e:
        print(f"error in recv/send try again {str(e)}")



while True:
    #wait to clients

    client_sock, addr = server_sock.accept()

    print(f"{addr[0]} - connected")
    # handle the client
    while True:
        try:
            data = client_sock.recv(1).decode()
            if data not in ['1','2']:
                break
            print(f"getting data - {data}")

            if data == "1":
                im = ImageGrab.grab()
                im.save('screenshot.jpg')
                with open('screenshot.jpg', 'rb') as file:
                    image_data = file.read()

                send_data(client_sock, 6, image_data)


            if data == "2":
                try:
                    app_len = int(client_sock.recv(2).decode())
                    app_name = client_sock.recv(app_len).decode()
                    print("f")
                    subprocess.call(data)
                except Exception as e:
                    print(f"error in recv/send try again {str(e)}")



        except Exception as e:
            print(f"error in recv/send try again {str(e)}")
    print(f"{addr[0]} - disconnected")
    client_sock.close()