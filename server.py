# ------- Bolierplate Code Start -----


import socket
from  threading import Thread
import time
IP_ADDRESS = '127.0.0.1'
PORT = 8080
SERVER = None
clients = {}
bufferSize = 4096

def handleMsg(client, msg, client_name):
    if msg == "show list":
        handle_client_list(client)



def handleClient(client, client_name):
    global clients
    global bufferSize
    global SERVER

    myMsg = "Welcome to File Transfer Protocol, you are connected with a server\n" \
            "Click on 'Refresh' button to see all the available clients\n" \
            "Click on indivual clients to start sharing the files"

    client.send(myMsg.encode("utf-8"))

    while True:
        try:
            buffersize = clients[client_name]["file_size"]
            junk = client.recv(buffersize)
            msg = junk.decode("utf-8").strip().lower()

            if msg:
                handleMsg(client, msg, client_name)


        except:
            pass


def acceptConnections():
    global SERVER
    global clients

    while True:
        client, addr = SERVER.accept()
        client_name = client.recv(4096).decode('utf').lower()
        clients[client_name] = {
            "client" : client,
            "address": addr,
            "file_name": "",
            "file_size": 4096,
            "connectedWith": ""

        }
        print(f"Connection established with {client_name}: {addr}")

        thread = Thread(target = handleClient, args =(client, client_name))
        thread.start()

def handle_client_list(client):
    global clients
    total = 0
    for i in clients:
        total += 1
        client_addr = clients[i]["address"][0]
        connectedwith = clients[i]["connectedWith"]
        smg = ""

        if connectedwith:
            smg = f"{total}, {i}, {client_addr},Connected with {connectedwith}"
        else:
            smg = f"{total}, {i}, {client_addr}, Available"
        client.send(smg.encode())
        time.sleep(1)


def setup():
    print("\n\t\t\t\t\t\tIP MESSENGER\n")

    # Getting global values
    global PORT
    global IP_ADDRESS
    global SERVER


    SERVER  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    SERVER.listen(100)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")

    acceptConnections()


setup_thread = Thread(target=setup)           #receiving multiple messages
setup_thread.start()

# ------ Bolierplate Code End -----------