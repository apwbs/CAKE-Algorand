import json
import socket
import ssl
from hashlib import sha512
from decouple import config
import sqlite3

# Connection to SQLite3 reader database
connection = sqlite3.connect('files/reader/reader.db')
x = connection.cursor()

process_instance_id = config('PROCESS_INSTANCE_ID')

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
server_sni_hostname = 'example.com'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "172.17.0.2"
ADDR = (SERVER, PORT)
server_cert = 'Keys/server.crt'
client_cert = 'Keys/client.crt'
client_key = 'Keys/client.key'

# connection = sqlite3.connect('Database_Reader/private_key.db')
# y = connection.cursor()

"""
creation and connection of the secure channel using SSL protocol
"""

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
conn.connect(ADDR)


"""
function to handle the sending and receiving messages.
"""


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)
    receive = conn.recv(6000).decode(FORMAT)
    if len(receive) != 0:
        if receive[:25] == 'Here is IPFS link and key':
            key = receive.split('\n\n')[0].split("b'")[1].rstrip("'")
            ipfs_link = receive.split('\n\n')[1]

            x.execute("INSERT OR IGNORE INTO decription_keys VALUES (?,?,?,?)",
                      (process_instance_id, message_id, ipfs_link, key))
            connection.commit()
        elif receive[:26] == 'Here is plaintext and salt':
            plaintext = receive.split('\n\n')[0].split('Here is plaintext and salt: ')[1]
            salt = receive.split('\n\n')[1]

            x.execute("INSERT OR IGNORE INTO plaintext VALUES (?,?,?,?,?)",
                      (process_instance_id, message_id, slice_id, plaintext, salt))
            connection.commit()


message_id = '5388148990832263896'
slice_id = '0'
requester = 'K2J47GKYN5CGNZWYIF6VO6AL63TLCB24JMZJAUMX63XPVQH4DU5IBN3GDE'

# msg = b'9139315610039915578'
# hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
# y.execute("SELECT * FROM privateKeys WHERE address = ?", (requester,))
# user_privateKey = y.fetchall()
# signature = pow(hash, int(user_privateKey[0][2]), int(user_privateKey[0][1]))

# send("Please certify signature||" + requester)


# send("Generate my key||" + message_id + '||' + requester)

send("Access my data||" + message_id + '||' + slice_id + '||' + requester)

# exit()

send(DISCONNECT_MESSAGE)
