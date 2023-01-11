import socket
import ssl
from hashlib import sha512
import sqlite3
import json
from decouple import config

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

# # Connection to SQLite3 data_owner database
# connection = sqlite3.connect('Database_Reader/data_owner.db')
# y = connection.cursor()

"""
creation and connection of the secure channel using SSL protocol
"""

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
conn.connect(ADDR)

manufacturer_address = config('ADDRESS_MANUFACTURER')

"""
function to handle the sending and receiving messages.
"""


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    # print(send_length)
    conn.send(message)
    receive = conn.recv(6000).decode(FORMAT)
    if len(receive) != 0:
        print(receive)


f = open('files/data.json')
g = open('files/data.json')

message_to_send = g.read()

entries = [['ID', 'SortAs', 'GlossTerm'], ['Acronym', 'Abbrev'], ['Specs', 'Dates']]
entries_string = '###'.join(str(x) for x in entries)

policy = ['1604423002081035210 and MANUFACTURER',
          '1604423002081035210 and (MANUFACTURER or (SUPPLIER and ELECTRONICS))',
          '1604423002081035210 and (MANUFACTURER or (SUPPLIER and MECHANICS))']
policy_string = '###'.join(policy)

# data = json.load(f)
# entries = list(data.keys())
# entries_string = '###'.join(entries)
# print(entries_string)
# exit()

# entries_string = ''

sender = manufacturer_address

send("Cipher this message||" + message_to_send + '||' + entries_string + '||' + policy_string + '||' + sender)

# send(DISCONNECT_MESSAGE)
