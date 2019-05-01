import socket

def listen():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(('0.0.0.0', 5555))
    connection.listen(10)
    while True:
        current_connection, address = connection.accept()
        while True:
            data = current_connection.recv(2048)
            data = data.decode("utf-8")

            if data == "quit":
                current_connection.shutdown(1)
                current_connection.close()
                break

            elif data == "stop":
                current_connection.shutdown(1)
                current_connection.close()
                exit()

            elif data:
                current_connection.send(data.encode("utf-8"))
                print(data)


if __name__ == "__main__":
    try:
        listen()
    except KeyboardInterrupt:
        pass
