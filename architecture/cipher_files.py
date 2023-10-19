from charm.toolbox.ABEnc import ABEnc
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.toolbox.pairinggroup import PairingGroup, GT
from charm.core.engine.util import objectToBytes, bytesToObject
from charm.toolbox.symcrypto import AuthenticatedCryptoAbstraction
from charm.core.math.pairing import hashPair as sha2, deserialize, serialize
import json
# import write
import sqlite3
# import encoders_decoders
import random
import rsa
import hashlib
import base64
import encoders_decoders
from datetime import datetime
import re
import ipfshttpclient
import os
import ast
from decouple import config

api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

app_id_messages = config('APPLICATION_ID_MESSAGES')
skm_address = config('SKM_ADDRESS')
sdm_private_key = config('SDM_PRIVATEKEY')


"""
Necessary ABE connections
"""


class HybridABEnc(ABEnc):

    def __init__(self, scheme, groupObj):
        ABEnc.__init__(self)
        # check properties (TODO)
        self.abenc = scheme
        self.group = groupObj

    def setup(self):
        return self.abenc.setup()

    def encrypt(self, pk, M, object):
        key = self.group.random(GT)
        c1 = self.abenc.encrypt(pk, key, object)
        cipher = AuthenticatedCryptoAbstraction(sha2(key))
        c2 = cipher.encrypt(M)
        return {'c1': c1, 'c2': c2}


"""
- creation of the "shared secret" between SDM and SKM, namely (pk,mk) keys
- ciphering of the message with the policy
- call to the "write" module to write the IPFS file with all necessary data of the message
"""


def main(message, access_policy, sender):
    groupObj = PairingGroup('SS512')
    cpabe = CPabe_BSW07(groupObj)
    hyb_abe = HybridABEnc(cpabe, groupObj)

    (pk, mk) = hyb_abe.setup()

    pk_bytes = objectToBytes(pk, groupObj)
    pk_bytes_64 = base64.b64encode(pk_bytes).decode('ascii')

    mk_bytes = objectToBytes(mk, groupObj)
    mk_bytes_encoded = encoders_decoders.mk_encoder(mk_bytes, skm_address)
    mk_bytes_encoded_64 = base64.b64encode(mk_bytes_encoded).decode('ascii')

    access_policy = access_policy.split('###')

    now = datetime.now()
    now = int(now.strftime("%Y%m%d%H%M%S%f"))
    random.seed(now)

    message_dict = json.loads(message)

    metadata_list = []
    ciphered_message_list = []
    final_slices = []
    for i, entry in enumerate(message_dict):
        ciphered_message = {}

        slice_id = random.randint(1, 2 ** 64)
        final_slices.append(slice_id)
        print(f'slice id: {slice_id}')

        cipher_field = hyb_abe.encrypt(pk, entry, access_policy[i])
        cipher_field_bytes = objectToBytes(cipher_field, groupObj)
        cipher_field_bytes_64 = base64.b64encode(cipher_field_bytes).decode('ascii')

        cipher = hyb_abe.encrypt(pk, message_dict[entry], access_policy[i])
        cipher_bytes = objectToBytes(cipher, groupObj)
        cipher_bytes_64 = base64.b64encode(cipher_bytes).decode('ascii')
        ciphered_message[cipher_field_bytes_64] = cipher_bytes_64
        ciphered_message_list.append(ciphered_message)

        salt = random.randint(1, 2 ** 64)
        salt_to_encrypt = str(salt).encode()
        salt_with_policy = hyb_abe.encrypt(pk, salt_to_encrypt, access_policy[i])
        salt_with_policy_bytes = objectToBytes(salt_with_policy, groupObj)
        salt_with_policy_bytes_64 = base64.b64encode(salt_with_policy_bytes).decode('ascii')

        s_1 = message_dict[entry] + str(salt)
        s_1 = s_1.encode()
        s_1_hashed = hashlib.sha256(s_1)
        hex_dig = s_1_hashed.hexdigest()

        metadata = {'slice_id': slice_id, 'message_with_salt': hex_dig, 'salt': salt_with_policy_bytes_64, 'file': cipher_field_bytes_64}
        metadata_list.append(metadata)

    message_id = random.randint(1, 2 ** 64)
    print(f'message id: {message_id}')

    header = {'sender': sender, 'message_id': message_id, 'pk': pk_bytes_64, 'mk': mk_bytes_encoded_64}

    final_message = {'header': header, 'metadata': metadata_list, 'body': ciphered_message_list}

    with open('files/more_files.json', 'w') as u1:
        u1.write(json.dumps(final_message))

    hash_file = api.add_json(final_message)
    print(f'ipfs hash: {hash_file}')

    os_result = os.popen('python3.10 blockchain/MessageContract/MessageContractMain.py -sender %s -app %s -message %s -hash %s' % (
        sdm_private_key, app_id_messages, message_id, hash_file)).read()
    print(os_result)
    tx_id = os_result.split('Transaction id: ')[1]
    return message_id, hash_file, final_slices, tx_id

