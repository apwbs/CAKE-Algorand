from MessageContract import *
from algosdk.atomic_transaction_composer import AtomicTransactionComposer
import sys

# sys.path.insert(0, '../')
# from util import *
sys.path.insert(1, 'blockchain/')
from util import *

# user declared account mnemonics
creator_mnemonic = "infant flag husband illness gentle palace eye tilt large reopen current purity enemy depart couch moment gate transfer address diamond vital between unlock able cave"
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "p8IwM35NPv3nRf0LLEquJ5tmpOtcC4he7KKnJ3wE"
headers = {
    "X-API-Key": algod_token,
}


def saveData(
        client: algod.AlgodClient,
        sender: str,
        app_id: int,
        message_id: str,
        hash_file: str,
) -> None:
    atc = AtomicTransactionComposer()
    signer = AccountTransactionSigner(sender)
    sp = client.suggested_params()

    app_args = [
        message_id,
        hash_file
    ]

    with open("blockchain/MessageContract/msg_contract.json") as f:
        js = f.read()
    atc.add_method_call(
        app_id=app_id,
        method=get_method('on_save', js),
        sender=account.address_from_private_key(sender),
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
    global_ints = 2
    global_bytes = 2
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)

    # Compile the program
    router = getRouter()
    approval_program, clear_program, contract = router.compile_program(version=6,
                                                                       optimize=OptimizeOptions(scratch_slots=True))

    with open("msg_approval.teal", "w") as f:
        f.write(approval_program)

    with open("msg_clear.teal", "w") as f:
        f.write(clear_program)

    with open("msg_contract.json", "w") as f:
        import json

        f.write(json.dumps(contract.dictify()))

    approval_program_compiled = compile_program(algod_client, approval_program)

    clear_state_program_compiled = compile_program(algod_client, clear_program)

    print("--------------------------------------------")
    print("Deploying application......")

    atc = AtomicTransactionComposer()
    signer = AccountTransactionSigner(senderSK)
    sp = algod_client.suggested_params()

    with open("msg_contract.json") as f:
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


def main(params):
    # sender_private_key = get_private_key_from_mnemonic(creator_mnemonic)
    sender_private_key = params[1]
    # sender_address = account.address_from_private_key(creator_private_key)

    algod_client = algod.AlgodClient(algod_token, algod_address, headers)

    # app_id, contract = createApp(algod_client, sender_private_key)
    # print('App id: ', app_id)

    print("--------------------------------------------")
    print("Saving message in the application......")
    app_id = params[2]
    message_id = params[3]
    hash_file = params[4]
    saveData(algod_client, sender_private_key, app_id, message_id, hash_file)


if __name__ == "__main__":
    # main()
    main(sys.argv)
