import socket
import ssl
import threading
import key_generation
import decipher_message
from datetime import datetime
import random
import sqlite3
from hashlib import sha512

HEADER = 64
PORT = 5050
server_cert = 'Keys/server.crt'
server_key = 'Keys/server.key'
client_certs = 'Keys/client.crt'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

"""
creation and connection of the secure channel using SSL protocol
"""

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=client_certs)
bindsocket = socket.socket()
bindsocket.bind(ADDR)
bindsocket.listen(5)


def generate(message_id, reader_address):
    return key_generation.main(message_id, reader_address)


def read(message_id, slice_id, reader_address):
    return decipher_message.main(message_id, slice_id, reader_address)


"""
function that handles the requests from the clients. There are two possible requests, namely the 
creation of a key and the deciphering of a ciphertext.
"""


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            # print(f"[{addr}] {msg}")
            conn.send("Msg received!".encode(FORMAT))
            message = msg.split('||')
            if message[0] == "Generate my key":
                response = generate(message[1], message[2])
                response_0 = bytes(str(response[0]), FORMAT)
                response_1 = bytes(str(response[1]), FORMAT)
                conn.send(b'Here is IPFS link and key: ' + response_0 + b'\n\n' + response_1)
            if message[0] == "Access my data":
                response = read(message[1], message[2], message[3])
                conn.send(b'Here is plaintext and salt:\n\n' + response[0] + b'\n\n' + response[1])

    conn.close()


"""
main function starting the server. It listens on a port and waits for a request from a client
"""


def start():
    bindsocket.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        newsocket, fromaddr = bindsocket.accept()
        conn = context.wrap_socket(newsocket, server_side=True)
        thread = threading.Thread(target=handle_client, args=(conn, fromaddr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
