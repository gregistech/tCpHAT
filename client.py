import socket
import sys
from threading import Thread

username = ""

class Server:
    def __init__(self, con):
        self.con = con

class ListeningThread(Thread):
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server
    def run(self):
        while True:
            connection = self.server.con
            data = connection.recv(2048)
            if not data: break
            data = data.decode("utf-8")
            print(data)
        return

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("127.0.0.1", 1242))
username = input("Your username: ")
connection.send(("/reg " + username).encode("utf-8"))
while True:
    listenThread = ListeningThread(Server(connection))
    listenThread.start()
    msg = input()
    connection.send(msg.encode("utf-8"))
