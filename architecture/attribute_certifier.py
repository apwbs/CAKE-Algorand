import json
from decouple import config
import ipfshttpclient
import os
import io
import sqlite3
from datetime import datetime
import random

api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

app_id_certifier = config('APPLICATION_ID_CERTIFIER')
certifier_private_key = config('CERTIFIER_PRIVATEKEY')

manufacturer_address = config('ADDRESS_MANUFACTURER')
supplier1_address = config('ADDRESS_SUPPLIER1')
supplier2_address = config('ADDRESS_SUPPLIER2')

# Connection to SQLite3 attribute_certifier database
conn = sqlite3.connect('files/attribute_certifier/attribute_certifier.db')
x = conn.cursor()


def generate_attributes():
    now = datetime.now()
    now = int(now.strftime("%Y%m%d%H%M%S%f"))
    random.seed(now)
    process_instance_id = random.randint(1, 2 ** 64)
    print(f'process instance id: {process_instance_id}')

    dict_users = {
        manufacturer_address: [str(process_instance_id), 'MANUFACTURER'],

        supplier1_address: [str(process_instance_id), 'SUPPLIER', 'ELECTRONICS'],

        supplier2_address: [str(process_instance_id), 'SUPPLIER', 'MECHANICS']
    }

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
        os.system('python3.10 blockchain/AttributeCertifierContract/AttributeCertifierContractMain.py %s %s %s %s' %
                  (certifier_private_key, app_id_certifier, process_instance_id, hash_file)))


if __name__ == "__main__":
    generate_attributes()
