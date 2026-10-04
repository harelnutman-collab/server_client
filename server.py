#git link - https://github.com/harelnutman-collab/server_client
import socket
import datetime
import random

#create the server
server_sock = socket.socket()
server_sock.bind(("0.0.0.0", 1451))
server_sock.listen(3)
func_tuple = ("time", "name", "rand")
server_name = "Harel's server"

while True:
    #wait to clients
    client_sock, addr = server_sock.accept()
    print(f"{addr[0]} - connected")
    # handle the client
    while True:
        try:
            data = client_sock.recv(4).decode()
            if data not in func_tuple:
                break
            print(f"getting data - {data}")
            #client_sock.send(data.encode())
            if data.lower() == "time":
                time = datetime.datetime.now()
                client_sock.send(str(time).encode())
            if data.lower() == "rand":
                number = random.randint(1,11)
                client_sock.send(str(number).encode())
            if data.lower() == "name":
                client_sock.send(server_name.encode())



        except Exception as e:
            print(f"error in recv/send {str(e)}")
            break

    print(f"{addr[0]} - disconnected")
    client_sock.close()