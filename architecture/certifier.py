from decouple import config
from Crypto.PublicKey import RSA
import ipfshttpclient
import sqlite3
import io
import rsa
import random
from datetime import datetime
import json
import os
import argparse

def store_process_id_to_env(value):
    name = 'PROCESS_INSTANCE_ID'
    with open('../.env', 'r', encoding='utf-8') as file:
        data = file.readlines()
    edited = False
    for line in data:
        if line.startswith(name):
            data.remove(line)
            break
    line = name + "=" + value + "\n"
    data.append(line)

    with open('../.env', 'w', encoding='utf-8') as file:
        file.writelines(data)

class Certifier():
    def certify(actors, roles):
        for actor in actors:
            Certifier.__read_public_key__(actor)
        Certifier.__skm_public_key__()
        return Certifier.__attribute_certification__(roles)


    def read_public_keys(actors):
        for actor in actors:
            Certifier.__read_public_key__(actor)

    def skm_public_key():
        Certifier.__skm_public_key__()

    def attribute_certification(roles):
        Certifier.__attribute_certification__(roles)


    def __read_public_key__(actor_name):
        api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

        print("Reading keys of " + actor_name)
        reader_address = config('ADDRESS_' + actor_name)
        private_key = config('PRIVATEKEY_' + actor_name)
        app_id_pk_readers = config('APPLICATION_ID_PK_READERS')

        # Connection to SQLite3 reader database
        conn = sqlite3.connect('files/reader/reader.db')
        x = conn.cursor()

        # # Connection to SQLite3 data_owner database
        connection = sqlite3.connect('files/data_owner/data_owner.db')
        y = connection.cursor()

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

    def __skm_public_key__():
        api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

        print("Reading keys of SKM")

        skm_address = config('SKM_ADDRESS')
        skm_private_key = config('SKM_PRIVATEKEY')

        app_id_pk_skm = config('APPLICATION_ID_PK_SKM')

        # Connection to SQLite3 reader database
        conn = sqlite3.connect('files/skm/skm.db')
        x = conn.cursor()

        (publicKey, privateKey) = rsa.newkeys(1024)
        publicKey_store = publicKey.save_pkcs1().decode('utf-8')
        privateKey_store = privateKey.save_pkcs1().decode('utf-8')

        f = io.StringIO()
        f.write('skm_address: ' + skm_address + '###')
        f.write(publicKey_store)
        f.seek(0)

        hash_file = api.add_json(f.read())
        print(f'ipfs hash: {hash_file}')

        x.execute("INSERT OR IGNORE INTO rsa_private_key VALUES (?,?)", (skm_address, privateKey_store))
        conn.commit()

        x.execute("INSERT OR IGNORE INTO rsa_public_key VALUES (?,?,?)", (skm_address, hash_file, publicKey_store))
        conn.commit()

        print(os.system('python3.10 blockchain/PublicKeySKM/PKSKMContractMain.py -creator %s -app %s -ipfs %s' % (
            skm_private_key, app_id_pk_skm, hash_file)))



    def __attribute_certification__(roles):

        app_id_certifier = config('APPLICATION_ID_CERTIFIER')

        api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001') # Connect to local IPFS node (creo un nodo locale di ipfs)

        app_id_certifier = config('APPLICATION_ID_CERTIFIER')
        certifier_private_key = config('CERTIFIER_PRIVATEKEY')

        # Connection to SQLite3 attribute_certifier database
        conn = sqlite3.connect('files/attribute_certifier/attribute_certifier.db') # Connect to the database
        x = conn.cursor()

        now = datetime.now()
        now = int(now.strftime("%Y%m%d%H%M%S%f"))
        random.seed(now)
        process_instance_id = random.randint(1, 2 ** 63)
        print(f'process instance id: {process_instance_id}')
        
        dict_users = {}
        for actor, list_roles in roles.items():
            dict_users[config('ADDRESS_' + actor)] = [str(process_instance_id)] + [role for role in list_roles]

        f = io.StringIO()
        dict_users_dumped = json.dumps(dict_users)
        f.write('"process_instance_id": ' + str(process_instance_id) + '####')
        f.write(dict_users_dumped)
        f.seek(0)

        file_to_str = f.read()

        hash_file = api.add_json(file_to_str)
        print(f'ipfs hash: {hash_file}')

        x.execute("INSERT OR IGNORE INTO user_attributes VALUES (?,?,?)",
                (str(process_instance_id), hash_file, file_to_str))
        conn.commit()
        print(
            os.system('python3.10 blockchain/AttributeCertifierContract/AttributeCertifierContractMain.py -sender %s -app %s -process %s -hash %s' %
                    (certifier_private_key, app_id_certifier, process_instance_id, hash_file)))
        
        print(f'process instance id: {process_instance_id}')

        store_process_id_to_env(str(process_instance_id))
        return process_instance_id

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Certifier configuration')
    parser.add_argument('-o', '--operation', type=int, default=0,help='Operation to perform \n 0 - READ PUBLIC KEY \n 2 - READ SKM PUBLIC KEY \n 3 - CERTIFY ATTRIBUTES ')
    parser.add_argument('-r', '--reader', type=str, default='MANUFACTURER',help='Reader name')
    args = parser.parse_args()
    if args.operation == 0:
        print(args.reader)
        Certifier.read_public_keys([args.reader])

    elif args.operation == 1:
        Certifier.skm_public_key()

    elif args.operation == 2:
        manufacturer_address = config('ADDRESS_MANUFACTURER')
        supplier1_address = config('ADDRESS_SUPPLIER1')
        supplier2_address = config('ADDRESS_SUPPLIER2')

        roles = {
            'MANUFACTURER': ['MANUFACTURER'],

            'SUPPLIER1': ['SUPPLIER', 'ELECTRONICS'],

            'SUPPLIER2': ['SUPPLIER', 'MECHANICS']
        }
        Certifier.attribute_certification(roles)
    else:
        raise Exception("Operation number not valid")    

