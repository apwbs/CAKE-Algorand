from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk import transaction
import argparse
from decouple import config

algod_address = config('ALGOD_ADDRESS')
algod_token = config('ALGOD_TOKEN')
headers = {
   "X-API-Key": algod_token,
}

roles = ['CERTIFIER', 'MANUFACTURER', 'SUPPLIER1', 'SUPPLIER2', 'SKM', 'SDM']


algod_client = algod.AlgodClient(algod_token, algod_address, headers)


def generate_algorand_keypair(role = "My"):
    private_key, address = account.generate_account()
    print(role + " address: {}".format(address))
    print(role +" private key: {}".format(private_key))
    print(role +" passphrase: {}".format(mnemonic.from_private_key(private_key)))
    print("\n")
    return address, private_key

parser = argparse.ArgumentParser()
parser.add_argument('-A' ,'--all', action='store_true')

args = parser.parse_args()

if args.all:
    if input("This operation will reset address and private key stored in .env, press y to continue or any other key to abort: ").lower() != 'y':
        exit()
    for role in roles:
        address, private_key =  generate_algorand_keypair(role + "'")

        with open('.env', 'r', encoding='utf-8') as file:
            data = file.readlines()
        for line in data:
            if line.startswith('ADDRESS_' + role):
                data.remove(line)
                break
        for line in data:
            if line.startswith(role + '_PRIVATEKEY'):
                data.remove(line)
                break
        line = 'ADDRESS_' + role + "=" + address + "\n"
        data.append(line)
        line = role + '_PRIVATEKEY=' + private_key + "\n"
        data.append(line)
        with open('.env', 'w', encoding='utf-8') as file:
            file.writelines(data)
    
    address, private_key =  generate_algorand_keypair('CREATOR' + '\'s')
    with open('.env', 'r', encoding='utf-8') as file:
        data = file.readlines()
    for line in data:
        if line.startswith('ADDRESS_CREATOR'):
            data.remove(line)
            break
    for line in data:
        if line.startswith('CREATOR_PRIVATEKEY'):
            data.remove(line)
            break
    line = "ADDRESS_CREATOR=" + address + "\n"
    data.append(line)
    line =  'CREATOR_PRIVATEKEY=' + private_key + "\n"
    data.append(line)

    passphrase = mnemonic.from_private_key(private_key)
    for line in data:
        if line.startswith('PASSPHRASE_CREATOR'):
            data.remove(line)
            break
    line = 'PASSPHRASE_CREATOR=' + passphrase + "\n"  
    data.append(line)
    with open('.env', 'w', encoding='utf-8') as file:
        file.writelines(data)

else:
    generate_algorand_keypair()