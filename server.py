import socket
from threading import Thread
from command import Command
from commands import *
clients = []

def sendAll(clients, msg): 
    for c in clients:
        try:
            c.con.send(msg.encode("utf-8"))
        except BrokenPipeError:
            clients.remove(c)
commands = {
            "disconnect": Command("disconnect", disconnect, 0),
            "reg": Command("reg", registerClient, 1)
        }

class Client: 
    def __init__(self, con, name):
        self.con = con
        self.name = name

class ListeningThread(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client
        self.connection = client.con
        self.name = client.name

    def run(self):
        client = self.client
        connection = self.connection 
        while True:
            if connection.fileno() == -1: return
            data = connection.recv(2048)
            if not data: return
            data = data.decode("utf-8")
            
            if data.startswith("/"):
                try:
                    data = data[1:]
                    params = data.split(" ")
                    com = params[0]
                    params = params[1:]
                    v = commands[com]
                except KeyError:
                    connection.send("Command not found... You should try the /help command.".encode("utf-8"))
                else: 
                    if len(params) == v.maxparams:
                        v.action(params, client)
                    else:
                        connection.send("This command needs {0} number of parameters, not {1}".format(v.maxparams, 
                                                                                                      len(params)).encode("utf-8"))
            else:
                clientsMod = clients.copy()
                clientsMod.remove(client)
                sendAll(clientsMod, client.name + ": " + data)
        connection.close()
        return

def listen():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.bind(('0.0.0.0', 1243))
    connection.listen(20)
    while True:
        c, address = connection.accept()
        curClient = Client(c, "Anonymus")
        clients.append(curClient)
        curThread = ListeningThread(curClient)
        curThread.start()

if __name__ == "__main__":
    try:
        listen()
    except KeyboardInterrupt:
        pass
