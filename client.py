import socket

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("127.0.0.1", 1237))
while True:
    msg = input("Message: ")
    connection.send(msg.encode("utf-8"))
    data = connection.recv(2048)
    if not data: break
    data = data.decode("utf-8")
    print(data)
