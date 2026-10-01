import socket


my_sock = socket.socket()
func_tuple = ("time", "name", "rand")

try:
    my_sock.connect(("127.0.0.1", 1450))
except Exception as e:
    my_sock.close()
    exit(f"server is down - try again {str(e)}")

while True:
    msg = input("enter msg to send or exit to finish ")
    if msg.lower() == "exit":
        break

    elif msg.lower() in func_tuple:
        my_sock.send(msg.encode())
        try:
            data = my_sock.recv(1024).decode()
            print(f"server send - {data}")

        except Exception as e:
            print(f"error in receive or sending data {str(e)}")
    else:
        print("illegal message")

my_sock.close()
print("bye bye")