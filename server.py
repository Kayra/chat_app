from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread

clients = {}
addresses = {}

HOST = ""
PORT = 33000
ADDR = (HOST, PORT)

BUFFERSIZE = 1024

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def accept_incoming_connections():
    """
    Sets up handling for incoming clients.
    """

    while True:

        client, client_address = SERVER.accept()
        print(f"{client}:{client_address} has connected.")

        client.send(bytes("Hello world. Please type your name and press enter.", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    """
    Handles a single client connection.
    """

    name = client.recv(BUFFERSIZE).decode("utf8")
    clients[client] = name

    welcome_message = f"Welcome {name}! If you ever want to quit, type <quit> (with angular brackets) to exit."
    client.send(bytes(welcome_message, "utf8"))

    joined_message = f"{name} has joined the chat!"
    broadcast(bytes(joined_message, "utf8"))

    while True:

        message = client.recv(BUFFERSIZE)

        if message != bytes("<quit>", "utf8"):
            broadcast(message, name + ": ")

        else:

            client.send(bytes("Quitting.", "utf8"))
            client.close()
            del clients[client]

            broadcast(bytes(f"{name} has left the chat.", "utf8"))

            break


def broadcast(message, prefix=""):
    """
    Broadcasts message to all connected clients.
    """

    for _socket in clients:
        _socket.send(bytes(prefix, "utf8") + message)


if __name__ == "__main__":

    SERVER.listen(5)
    print("Waiting for connection...")

    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()

    SERVER.close()
