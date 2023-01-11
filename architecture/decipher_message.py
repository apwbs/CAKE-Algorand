from charm.toolbox.ABEnc import ABEnc
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.toolbox.pairinggroup import PairingGroup, GT
from charm.toolbox.symcrypto import AuthenticatedCryptoAbstraction
from charm.core.math.pairing import hashPair as sha2
from charm.core.engine.util import objectToBytes, bytesToObject
import json
import sqlite3
import ipfshttpclient
import retriever
# import decoders_encoders
from decouple import config
import re
import rsa
import base64
# import SC_retrieve_link

app_id_messages = config('APPLICATION_ID_MESSAGES')


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

    def decrypt(self, pk, sk, ct):
        c1, c2 = ct['c1'], ct['c2']
        key = self.abenc.decrypt(pk, sk, c1)
        if key is False:
            return b' '
            # raise Exception("failed to decrypt!")
        cipher = AuthenticatedCryptoAbstraction(sha2(key))
        return cipher.decrypt(c2)


"""
"""


def main(message_id, reader_address):
    api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
    global groupObj
    groupObj = PairingGroup('SS512')
    cpabe = CPabe_BSW07(groupObj)
    hyb_abe = HybridABEnc(cpabe, groupObj)

    msg_ipfs_link = retriever.retrieveMessage(app_id_messages, int(message_id))
    ciphertext_link = msg_ipfs_link[0]
    getfile1 = api.cat(ciphertext_link)
    j2 = json.loads(getfile1)

    pk = j2['header']['pk'].encode()
    pk = base64.b64decode(pk)
    pk = bytesToObject(pk, groupObj)

    body = json.loads(j2['body'])

    # salt = body[1][0][0][2]
    # salt = base64.b64decode(salt)
    # salt = bytesToObject(salt, groupObj)
    # print(salt)
    # exit()

    message = body[1][1]
    message = base64.b64decode(message)
    message = bytesToObject(message, groupObj)
    # print(type(message))
    # exit()

    sk = b'eJylVj1PXDEQ/Cunq6+w/fyxpg0USChBkFQROpGIJqKIciRShPjv8ezOvmehNIji7t492+vdmdmxn/fn+7Pd8/54/P54fzodj+Pf/tvfp4fT/rAbb//cP/5+0LdfSzjsihx2rY7f5bCLsR92WfDQxleIeBrv28LxUPGlE8phV8dshIgBs+OYXcZHGlfhQcbcOj4yFkriOn1I+s+Hmn0aImJ9ikyiY7OQ8Q87xfHUGpNEiLwwUQmeGma3gocRrY2hFrixLrfasLZWjw8cxlDvXKXDJbIqASrdMsU0yx1YoHod8RcIib2BFgrBr2SmWIrFULyqIjyGK5CMdy+DnPMfylysIee0hJCCjCklxfBWRmNIhEMi92nrztWoAyz66yVpwomzDJiFDAN81KLFAv9m66AMKcRJieEEQGlYBUPE8iiGpiKutASu0yEbd9g8QhSCi9gxAuFkymrBp3RLRblVJl2/mKJbR+ocbBRKtVIgqMBYWqzwVwptzm53zrppVWEGZNhiIvL2y/X11eXFzZtpUxgrC2nyuiOwXQ9MIkZP0HpzMVD0tVUTGNGmq7BBLeIhChpTaY6Vw9lb24KsqnGSQGb21kZmMytbhOBJW4aeBmpBPJCjpjCLR6ch7eZdhihK3UpElq2joD4gD+gaS0dPiSecmZ+RxqDYDqtUe2kVISklexdXFx8+33z6ePnh9q0Emsd5a6sKoU1sWWU1qNUlmVH2oeImpTnGTWhwN5nemS27LWIfJSuRiu4sbFallHE/iqmzGW1OYF802lqjlZrDZu5PD8BMZcOtFZk3tnpnSpgM2WBM261OegJP6oEmnWxvGn3XcCTNTZhyaVN92F5bjm1nBvrzvQ6q1YkbUqLT4AMxKUJswlqpcLc3908wrWcjDwHV+uwY3d3TTymEVjmqCvKy0aB1V74Ul3UhqQpRduPTcJGsuGoKWSuuoLS1WJ+aUKsSzk3cWPgH4gHOmc5uLsyzTrabgWtGePBgCMnrkZh5hNCBmrzbNjeuwupviS0nfU1oYQLeJX7ZYHJemBKgkAU/oTpHIo9NsyOeHibjhY2QZy+p3spxq1m7ohOPQGzz6gk8Gb3RjdTsBt3dP5zJ6IujIZlnsxTeZZqv9XtZ8buZXal0cXLndjdejw09Zv3Wtd62miP8Psd07hBFKBnkrMdb9AulOAy8jBIQPXeW6ZyWuqlXbYb3RBMq/Sg7JCbWMgG03hfsJpc3qrIfqZZBcPuU6MEyI2qbsx+EV2PhAdl40TMC6xRDZNNZK9M1uGyqVR2Lr7Szn0Xabbd6W4q9Xe/guiBS9O3VRUVbDlzsT0+/zv7nmWMChta+5P+Z7ruXf6wibQk='
    sk = bytesToObject(sk, groupObj)

    mdec = hyb_abe.decrypt(pk, sk, message)
    print(mdec)
    exit()
