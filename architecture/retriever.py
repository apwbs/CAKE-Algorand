from algosdk.v2client import indexer
import base64
from algosdk.encoding import decode_address, encode_address

indexer_address = "https://testnet-algorand.api.purestake.io/idx2"
indexer_token = ""
headers = {
    "X-API-Key": "p8IwM35NPv3nRf0LLEquJ5tmpOtcC4he7KKnJ3wE"
}

indexer_client = indexer.IndexerClient(indexer_token, indexer_address, headers)

name = 'test'
limit = 1


def retrieveReaderAttributes(application_id, process_instance_id):
    response = indexer_client.search_transactions(application_id=application_id)
    response['transactions'].reverse()
    for i in range(len(response['transactions'])):
        if i != 3:
            part = response['transactions'][i]['global-state-delta']
            if base64.b64decode(part[1]['key']) == b'process_id':
                if 'bytes' in part[1]['value']:
                    if int(base64.b64decode(part[1]['value']['bytes'])) == int(process_instance_id):
                        return base64.b64decode(part[0]['value']['bytes']).decode('utf-8')


def retrieveMessage(application_id, message_id):
    response = indexer_client.search_transactions(application_id=application_id)
    for i in range(len(response['transactions'])):
        part = response['transactions'][i]['global-state-delta']
        if base64.b64decode(part[1]['key']) == b'msg_id':
            if 'bytes' in part[1]['value']:
                if int(base64.b64decode(part[1]['value']['bytes'])) == int(message_id):
                    return base64.b64decode(part[0]['value']['bytes']).decode('utf-8'), \
                        response['transactions'][i]['sender']


def retrieveSKMPublicKey(application_id, skm_address):
    response = indexer_client.search_transactions(application_id=application_id)
    response['transactions'].reverse()
    for i in range(len(response['transactions'])):
        part = response['transactions'][i]['global-state-delta']
        if base64.b64decode(part[0]['key']) == b'pk_ipfs_link':
            if 'bytes' in part[1]['value']:
                if encode_address(base64.b64decode(part[1]['value']['bytes'])) == skm_address:
                    return base64.b64decode(part[0]['value']['bytes']).decode('utf-8')
