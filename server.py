#git link - https://github.com/harelnutman-collab/server_client
import socket
import datetime
import random

#create the server
server_sock = socket.socket()
server_sock.bind(("0.0.0.0", 1450))
server_sock.listen(3)
server_name = "Harel's server"

while True:
    #wait to clients
    client_sock, addr = server_sock.accept()
    print(f"{addr[0]} - connected")
    # handle the client
    while True:
            try:
                data = client_sock.recv(4).decode()
            except Exception as e:
                print(f"error in recv/send {str(e)}")
                break


            print(f"getting data - {data}")
            #client_sock.send(data.encode())
            if data.lower() == "time":
                answer = str(datetime.datetime.now())
            elif data.lower() == "rand":
                answer = str(random.randint(1,11))
            elif data.lower() == "name":
                answer = server_name
            else:
                break
            try:
                client_sock.send(str(len(answer)).zfill(2).encode())
                client_sock.send(str(answer).encode())
            except Exception as e:
                print(f"error in recv/send {str(e)}")
                break

    print(f"{addr[0]} - disconnected")
    client_sock.close()