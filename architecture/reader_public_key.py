from decouple import config
import os
from Crypto.PublicKey import RSA
from hashlib import sha512
import ipfshttpclient
import sqlite3
import io
import argparse

api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
app_id_pk_readers = config('APPLICATION_ID_PK_READERS')

'''
manufacturer_address = config('ADDRESS_MANUFACTURER')
manufacturer_private_key = config('PRIVATEKEY_MANUFACTURER')
electronics_address = config('ADDRESS_SUPPLIER1')
electronics_private_key = config('PRIVATEKEY_SUPPLIER1')
mechanics_address = config('ADDRESS_SUPPLIER2')
mechanics_private_key = config('PRIVATEKEY_SUPPLIER2')

reader_address = mechanics_address
private_key = mechanics_private_key
'''

parser = argparse.ArgumentParser(description='Reader name')
parser.add_argument('-r', '--reader', type=str, default='MANUFACTURER',help='Reader name')

args = parser.parse_args()
reader_address = config('ADDRESS_' + args.reader)
private_key = config('PRIVATEKEY_' + args.reader)
print(reader_address)
print(private_key)
print(args.reader)

# Connection to SQLite3 reader database
conn = sqlite3.connect('files/reader/reader.db')
x = conn.cursor()

# # Connection to SQLite3 data_owner database
connection = sqlite3.connect('files/data_owner/data_owner.db')
y = connection.cursor()


def generate_keys():
    keyPair = RSA.generate(bits=1024)
    # print(f"Public key:  (n={hex(keyPair.n)}, e={hex(keyPair.e)})")
    # print(f"Private key: (n={hex(keyPair.n)}, d={hex(keyPair.d)})")

    f = io.StringIO()
    f.write('reader_address: ' + reader_address + '###')
    f.write(str(keyPair.n) + '###' + str(keyPair.e))
    f.seek(0)

    hash_file = api.add_json(f.read())
    print(f'ipfs hash: {hash_file}')

    x.execute("INSERT OR IGNORE INTO rsa_private_key VALUES (?,?,?)", (reader_address, str(keyPair.n), str(keyPair.d)))
    conn.commit()

    x.execute("INSERT OR IGNORE INTO rsa_public_key VALUES (?,?,?,?)",
              (reader_address, hash_file, str(keyPair.n), str(keyPair.e)))
    conn.commit()

    y.execute("INSERT OR IGNORE INTO rsa_private_key VALUES (?,?,?)", (reader_address, str(keyPair.n), str(keyPair.d)))
    connection.commit()

    y.execute("INSERT OR IGNORE INTO rsa_public_key VALUES (?,?,?,?)",
              (reader_address, hash_file, str(keyPair.n), str(keyPair.e)))
    connection.commit()

    print('private key: ' + private_key)
    print(os.system('python3.10 blockchain/PublicKeysReadersContract/PKReadersContractMain.py -creator %s -app %s -ipfs %s' % (
        private_key, app_id_pk_readers, hash_file)))
    
if __name__ == "__main__":
    generate_keys()
