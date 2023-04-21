from PKSKMContract import *
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

    with open("blockchain/PublicKeySKM/pk_skm_contract.json") as f:
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

    print("Global state:", read_global_state(client, app_id))


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

    with open("pk_skm_approval.teal", "w") as f:
        f.write(approval_program)

    with open("pk_skm_clear.teal", "w") as f:
        f.write(clear_program)

    with open("pk_skm_contract.json", "w") as f:
        import json

        f.write(json.dumps(contract.dictify()))

    approval_program_compiled = compile_program(algod_client, approval_program)

    clear_state_program_compiled = compile_program(algod_client, clear_program)

    print("--------------------------------------------")
    print("Deploying application......")

    atc = AtomicTransactionComposer()
    signer = AccountTransactionSigner(senderSK)
    sp = algod_client.suggested_params()

    with open("pk_skm_contract.json") as f:
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

    print("Global state:", read_global_state(algod_client, app_id))

    assert app_id is not None and app_id > 0
    return app_id, contract



def deploy():
    sender_private_key = get_private_key_from_mnemonic(creator_mnemonic)

    algod_client = algod.AlgodClient(algod_token, algod_address, headers)

    app_id, contract = createApp(algod_client, sender_private_key)
    print('App id: ', app_id)
#    print('Set APPLICATION_ID_PK_SKM = ' + str(app_id) + ' in .env')
    set_application_id('APPLICATION_ID_PK_SKM', app_id)


def main(params):
    sender_private_key = params[1]

    algod_client = algod.AlgodClient(algod_token, algod_address, headers)
    print("--------------------------------------------")
    print("Saving message in the application......")
    app_id = params[2]
    message_id = params[3]
    hash_file = params[4]
    saveData(algod_client, sender_private_key, app_id, message_id, hash_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d' ,'--deploy', action='store_true')
    args = parser.parse_args()
    sys.path.insert(1, 'blockchain/')
    from util import *
    if args.deploy:
        deploy()
    else:
        main(sys.argv)
