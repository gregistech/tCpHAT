import socket
from threading import Thread
from command import Command

clients = []

def disconnect(client):
    client.con.close()

def sendAll(clients, msg): 
    for c in clients:
        c.con.send(msg.encode("utf-8"))

commands = {
            "disconnect": Command("disconnect", disconnect)
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
        while True:
            connection = self.connection
            if connection.fileno() == -1: return
            data = connection.recv(2048)
            if not data: return
            data = data.decode("utf-8")
            
            if data.startswith("/"):
                try:
                    data = data[1:]
                    v = commands[data]
                except KeyError:
                    connection.send("Command not found... You should try the /help command.".encode("utf-8"))
                else: 
                    v.action(self.client)
            else:
                clientsMod = clients.copy()
                clientsMod.remove(self.client)
                sendAll(clientsMod, data)
        connection.close()
        return

def listen():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.bind(('0.0.0.0', 1239))
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
