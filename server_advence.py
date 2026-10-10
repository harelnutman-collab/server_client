#git link - https://github.com/harelnutman-collab/server_client
import os.path
import socket
from PIL import ImageGrab
import subprocess
import pyperclip
import shutil
import psutil

server_sock = socket.socket()
server_sock.bind(("0.0.0.0", 1452))
server_sock.listen(3)


def check_if_process_running(process_name):
    for process in psutil.process_iter(['name']):
        if process.info['name'] == process_name:
            return True
    return False


def send_data(client, data_len_byte, data):
    if type(data) == str:
        data = data.encode()
    try:
      client.send(str(len(data)).zfill(data_len_byte).encode())
      client.send(data)
    except Exception as e:
        print(f"error in recv/send try again {str(e)}")


options_server = ['1', '2', '3', '4', '5', '6', '7']

while True:
    #wait to clients

    client_sock, addr = server_sock.accept()

    print(f"{addr[0]} - connected")
    # handle the client
    while True:
        try:
            data = client_sock.recv(1).decode()
            if data not in options_server:
                break
            print(f"getting data - {data}")

            if data == "1":
                im = ImageGrab.grab()
                im.save('screenshot.jpg')
                with open('screenshot.jpg', 'rb') as file:
                    image_data = file.read()

                send_data(client_sock, 6, image_data)


            elif data == "2":
                try:
                    app_len = int(client_sock.recv(2).decode())
                    app_name = str(client_sock.recv(app_len).decode())
                except Exception as e:
                    print(f"error in recv/send try again {str(e)}")
                    continue
                print(f"getting data - {str(app_name)}")
                try:
                    subprocess.call(app_name)
                except Exception as e:
                    print(f"app not open {str(e)}")
                    continue

                if check_if_process_running(app_name):
                    run = '0'
                else:
                    run = '1'

                try:
                    send_data(client_sock, 1, run)
                except Exception as e:
                    print(f"error in recv/send try again {str(e)}")
                    continue

            elif data == "3":
                try:
                    text_to_copy_len = int(client_sock.recv(3).decode())
                    text_to_copy = client_sock.recv(text_to_copy_len).decode()
                except Exception as e:
                    print(f"error in recv/send try again {str(e)}")
                    continue
                print(f"getting data - {str(text_to_copy)}")
                pyperclip.copy(text_to_copy)

            elif data == "4":

                paste_text = pyperclip.paste()
                print(paste_text)
                try:
                    print(f"getting data - {str(paste_text)}")
                    send_data(client_sock, 3, paste_text)
                except Exception as e:
                    print(f"error in recv/send try again {str(e)}")
                    continue

            elif data == "5":
                try:
                    file_name_len = int(client_sock.recv(2).decode())
                    file_path = str(client_sock.recv(file_name_len).decode())
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        send_data(client_sock, 1, '0')
                    else:
                        send_data(client_sock, 1, '1')
                except Exception as e:
                    print(f"error in recv/send try again {str(e)}")
                    continue

            elif data == "6":
                try:
                    folder_len = int(client_sock.recv(2).decode())
                    folder_name = str(client_sock.recv(folder_len).decode())
                except Exception as e:
                    print(f"error in recv/send try again {str(e)}")
                    continue


                if os.path.exists(folder_name):
                    files_list = str(os.listdir(folder_name))
                else:
                     files_list = "folder not exist"

                try:
                    send_data(client_sock, 4, files_list)
                except Exception as e:
                    print(f"error in recv/send try again {str(e)}")
                    continue

            elif data == "7":
                try:
                    file_one_len = int(client_sock.recv(2).decode())
                    file_one_name = str(client_sock.recv(file_one_len).decode())
                    file_two_len = int(client_sock.recv(2).decode())
                    file_two_name = str(client_sock.recv(file_two_len).decode())

                except Exception as e:
                    print(f"error in recv/send try again {str(e)}")
                    continue

                if os.path.exists(file_one_name):
                    shutil.copy(file_one_name, file_two_name)
                    complete = '0'
                else:
                    complete = '1'
                try:
                    send_data(client_sock, 1, complete)
                except Exception as e:
                    print(f"error in recv/send try again {str(e)}")
                    continue

        except Exception as e:
            print(f"error in recv/send try again {str(e)}")
    print(f"{addr[0]} - disconnected")
    client_sock.close()