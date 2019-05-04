import socket
import sys
from termcolor import colored
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
            
            escapedCharacters = []
            count = 0
            for i in data:
                if i == "\\":
                    if count < len(data) - 1:
                        if data[count + 1] == "|":
                            data = data[:count] + " " + data[count + 2:]
                            escapedCharacters.append(count)
                count += 1
            meta = data.split("|")
            
            for i in escapedCharacters:
                meta[2] = data[:i] + "|" + data[i + 2:]
                meta[2] = meta[2][len(meta[0]) + len(meta[1]) + 2:]
            if meta[0] == "msg":
                sender = colored(meta[1] + ": ", "yellow")
                msg = meta[2]
                print(sender + msg)
        return

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("127.0.0.1", 1243))
username = input("Your username: ")
connection.send(("/reg " + username).encode("utf-8"))
while True:
    listenThread = ListeningThread(Server(connection))
    listenThread.start()
    msg = input()
    connection.send(msg.encode("utf-8"))
