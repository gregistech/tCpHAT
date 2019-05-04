
def disconnect(params, client):
    client.con.close()

def registerClient(params, client):
    client.name = params[0]
