import socket 
from threading import Thread

host='127.0.0.1' # local host ip
port=8080
clients={}
addresses={}

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.bind((host, port))

def handle_clients(connection, addr):
    name = connection.recv(1024).decode()
    welcome = "Welcome " + name + ". You can type #quit if you ever want to leave the Chat Room"
    connection.recv(bytes(welcome, "utf8"))
    msg = name + " has recently joined the chatroom"
    broadcast(bytes(msg,"utf8"))
    clients[connection] = name

    while True:
        msg = connection.recv(1024)
        if msg!=bytes("#quit", "utf8"):
            broadcast(msg, name +":")
        else:
            connection.send(bytes("#quit", "utf8"))
            connection.close()
            del clients[connection]
            broadcast(bytes(name + " has left the chatroom.", "utfg8"))


def accept_client_connection():
    while True:
        client_connection, client_addr = socket_server.accept()
        print(client_addr, " has connected")
        client_connection.send("Welcome to the Chat Room, Please type your name to continue".encode('utf8'))
        addresses[client_connection] = client_addr

        Thread(target=handle_clients, args=(client_connection, client_addr)).start()

def broadcast(msg, prefix=""):
    for client in clients:
        client.send(bytes(prefix, "utf8")+msg)

if __name__=="__main__":
    socket_server.listen(5)
    print("The server is running and is listening to client's requests")

    t1 = Thread(target=accept_client_connection)
    t1.start()
    t1.join()

