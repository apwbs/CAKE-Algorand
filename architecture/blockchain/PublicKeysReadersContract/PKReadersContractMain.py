from PKReadersContract import *
from algosdk.atomic_transaction_composer import AtomicTransactionComposer
import sys
import argparse
from decouple import config


# user declared account mnemonics
creator_mnemonic = config('PASSPHRASE_CREATOR')
algod_address = config('ALGOD_ADDRESS')
algod_token = config('ALGOD_TOKEN')
headers = {
    "X-API-Key": algod_token,
}


def saveData(
        client: algod.AlgodClient,
        creator: str,
        app_id: int,
        r_address: str,
        firstElement: str,
) -> None:
    atc = AtomicTransactionComposer()
    signer = AccountTransactionSigner(creator)
    sp = client.suggested_params()

    app_args = [
        r_address,
        firstElement
    ]

    with open("blockchain/PublicKeysReadersContract/pk_readers_contract.json") as f:
        js = f.read()
    atc.add_method_call(
        app_id=app_id,
        method=get_method('on_save', js),
        sender=account.address_from_private_key(creator),
        sp=sp,
        signer=signer,
        method_args=app_args
    )

    result = atc.execute(client, 10)

    print("Transaction id:", result.tx_ids[0])

    #print("Global state:", read_global_state(client, app_id))


def createApp(
        algod_client: algod.AlgodClient,
        senderSK: str,
) -> int:
    local_ints = 0
    local_bytes = 0
    global_ints = 1
    global_bytes = 3
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)

    # Compile the program
    router = getRouter()
    approval_program, clear_program, contract = router.compile_program(version=6,
                                                                       optimize=OptimizeOptions(scratch_slots=True))

    with open("pk_readers_approval.teal", "w") as f:
        f.write(approval_program)

    with open("pk_readers_clear.teal", "w") as f:
        f.write(clear_program)

    with open("pk_readers_contract.json", "w") as f:
        import json

        f.write(json.dumps(contract.dictify()))

    approval_program_compiled = compile_program(algod_client, approval_program)

    clear_state_program_compiled = compile_program(algod_client, clear_program)

    print("--------------------------------------------")
    print("Deploying application......")

    atc = AtomicTransactionComposer()
    signer = AccountTransactionSigner(senderSK)
    sp = algod_client.suggested_params()

    with open("pk_readers_contract.json") as f:
        js = f.read()

    atc.add_method_call(
        app_id=0,
        method=get_method("create_app", js),
        sender=account.address_from_private_key(senderSK),
        sp=sp,
        signer=signer,
        approval_program=approval_program_compiled,
        clear_program=clear_state_program_compiled,
        local_schema=local_schema,
        global_schema=global_schema,
    )

    result = atc.execute(algod_client, 10)
    app_id = transaction.wait_for_confirmation(algod_client, result.tx_ids[0])['application-index']
    print("Transaction id:", result.tx_ids[0])

    #print("Global state:", read_global_state(algod_client, app_id))

    assert app_id is not None and app_id > 0
    return app_id, contract



def deploy():
    creator_private_key = get_private_key_from_mnemonic(creator_mnemonic)
    algod_client = algod.AlgodClient(algod_token, algod_address, headers)

    app_id, _ = createApp(algod_client, creator_private_key)
    print('App id: ', app_id)
    #print('Set APPLICATION_ID_PK_READERS = ' + str(app_id) + ' in .env'))
    set_application_id('APPLICATION_ID_PK_READERS', app_id)


def main(creator_private_key, app_id, ipfs_link):
    creator_address = account.address_from_private_key(creator_private_key)

    algod_client = algod.AlgodClient(algod_token, algod_address, headers)
    print("--------------------------------------------")
    print("Saving message in the application......")

    saveData(algod_client, creator_private_key, app_id, creator_address, ipfs_link)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d' ,'--deploy', action='store_true')
    parser.add_argument('-creator', '--creator_private_key', type=str, default='', help='Sender private key')
    parser.add_argument('-app', '--app_id', type=str, default='', help='App id of the contract')
    parser.add_argument('-ipfs', '--ipfs_link', type=str, default='', help='')


    args = parser.parse_args()
    sys.path.insert(1, 'blockchain/')
    sys.path.insert(0, '../')
    from util import *
    if args.deploy:
        deploy()
        exit()
    
    main(args.creator_private_key, args.app_id, args.ipfs_link)