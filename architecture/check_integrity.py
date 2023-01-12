import hashlib
import sqlite3
from decouple import config
import ipfshttpclient
import json

api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

process_instance_id = config('PROCESS_INSTANCE_ID')

# Connection to SQLite3 reader database
connection = sqlite3.connect('files/reader/reader.db')
x = connection.cursor()


def check_plaintext(process_instance_id, message_id, slice_id):
    x.execute("SELECT * FROM decription_keys WHERE process_instance=? AND message_id=?",
              (str(process_instance_id), str(message_id)))
    result = x.fetchall()
    message_ipfs_link = result[0][2]
    getfile = api.cat(message_ipfs_link)
    j2 = json.loads(getfile)
    body = json.loads(j2['body'])

    for i, elem in enumerate(body):
        slice_number = body[i][0][0][0]
        if slice_number == int(slice_id):
            message_hex = body[i][0][0][1]

            x.execute("SELECT * FROM plaintext WHERE process_instance=? AND message_id=? AND slice_id=?",
                (str(process_instance_id), str(message_id), str(slice_id)))
            result = x.fetchall()
            plaintext = result[0][3]
            salt = result[0][4]

            combined = plaintext + salt
            combined = combined.encode()
            combined_hashed = hashlib.sha256(combined)
            hex_dig = combined_hashed.hexdigest()

            print(hex_dig == message_hex)


if __name__ == "__main__":
    message_id = 9526055073375559011
    slice_id = 1678196926691841096
    check_plaintext(process_instance_id, message_id, slice_id)
