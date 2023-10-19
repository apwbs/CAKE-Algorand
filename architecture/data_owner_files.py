import socket
import ssl
import sys
from hashlib import sha512
import sqlite3
import json
import string
import random
import base64
import os
from decouple import config
import sqlite3
import argparse

## PENSO SIA DA TOGLIERE
# # Connection to SQLite3 reader database
# connection = sqlite3.connect('files/reader/reader.db')
# x = connection.cursor()

process_instance_id = config('PROCESS_INSTANCE_ID')
# print("process_instance_id: " + process_instance_id + "\n\n")

HEADER = 64
PORT = 5054
FORMAT = 'utf-8'
server_sni_hostname = config('SERVER_SNI_HOSTNAME')
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "10.181.120.137"
ADDR = (SERVER, PORT)
server_cert = 'Keys/server.crt'
client_cert = 'Keys/client.crt'
client_key = 'Keys/client.key'

# Connection to SQLite3 data_owner database
connection = sqlite3.connect('files/data_owner/data_owner.db')
x = connection.cursor()

"""
creation and connection of the secure channel using SSL protocol
"""

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
conn.connect(ADDR)

manufacturer_address = config('ADDRESS_MANUFACTURER')
sender = manufacturer_address


def sign_number():
    x.execute("SELECT * FROM handshake_number WHERE process_instance=?", (process_instance_id,))
    result = x.fetchall()
    number_to_sign = result[0][2]

    x.execute("SELECT * FROM rsa_private_key WHERE reader_address=?", (sender,))
    result = x.fetchall()
    private_key = result[0]

    private_key_n = int(private_key[1])
    private_key_d = int(private_key[2])

    msg = bytes(str(number_to_sign), 'utf-8')
    hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
    signature = pow(hash, private_key_d, private_key_n)
    # print("Signature:", hex(signature))
    return signature


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
    # print(receive)
    if len(receive) != 0:
        if receive.startswith('Number to be signed: '):
            len_initial_message = len('Number to be signed: ')
            x.execute("INSERT OR IGNORE INTO handshake_number VALUES (?,?,?)",
                      (process_instance_id, sender, receive[len_initial_message:]))
            connection.commit()
        if receive.startswith('Here is the message_id:'):
            x.execute("INSERT OR IGNORE INTO messages VALUES (?,?,?)", (process_instance_id, receive[24:], sender))
            connection.commit()


def file_to_base64(file_path):
    try:
        with open(file_path, 'rb') as file:
            encoded = base64.b64encode(file.read()).decode('utf-8')
        return encoded
    except Exception as e:
        print(f"Error encoding file to Base64: {e}")
        return None


def more_files_encryption():
    folder_path = "files/files_inputs/ok_files/"
    encoded_files = {}
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            encoded_data = file_to_base64(file_path)
            if encoded_data is not None:
                encoded_files[filename] = encoded_data

    message_to_send = json.dumps(encoded_files)

    policy = [process_instance_id + ' and (MANUFACTURER or SUPPLIER)',
              process_instance_id + ' and (MANUFACTURER or (SUPPLIER and ELECTRONICS))',
              process_instance_id + ' and (MANUFACTURER or (SUPPLIER and MECHANICS))']
    policy_string = '###'.join(policy)

    parser = argparse.ArgumentParser()
    parser.add_argument('-hs', '--handshake', action='store_true')
    parser.add_argument('-c', '--cipher', action='store_true')

    args = parser.parse_args()
    if args.handshake:
        send("Start handshake§" + sender)

    if args.cipher:
        signature_sending = sign_number()
        send(
            "Cipher these files§" + message_to_send + '§' + policy_string + '§' + sender + '§' + str(signature_sending))


more_files_encryption()
send(DISCONNECT_MESSAGE)
