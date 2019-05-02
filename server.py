import socket
from threading import Thread

class Client: 
    def __init__(self, con, name):
        self.con = con
        self.name = name

class ListeningThread(Thread):
    def __init__(self, connection):
        Thread.__init__(self)
        self.connection = connection

    def run(self):
        while True:
            connection = self.connection
            data = connection.recv(2048)
            connection.send(data)
        connection.close()

def listen():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.bind(('0.0.0.0', 1234))
    connection.listen(10)
    while True:
        c, address = connection.accept()
        curThread = ListeningThread(c)
        curThread.start()

if __name__ == "__main__":
    try:
        listen()
    except KeyboardInterrupt:
        pass
