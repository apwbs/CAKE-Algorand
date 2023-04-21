from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk import transaction

algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "2HrTwpGLLo3Ty5jqxsI2LhQ4aua1EPt1m2NVc4Bb"
headers = {
   "X-API-Key": algod_token,
}

algod_client = algod.AlgodClient(algod_token, algod_address, headers)


def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My private key: {}".format(private_key))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))

generate_algorand_keypair()