import socket


my_sock = socket.socket()

try:
    my_sock.connect(("127.0.0.1", 1450))
except Exception as e:
    my_sock.close()
    exit(f"server is down - try again {str(e)}")

while True:
    msg = input("enter msg to send or q to finish ")
    if msg.lower() == "q":
        break

    try:
        my_sock.send(msg.encode())
        data = my_sock.recv(1024).decode()
        print(f"server send - {data}")

    except Exception as e:
        print(f"error in receive or sending data {str(e)}")


my_sock.close()
print("bye bye")