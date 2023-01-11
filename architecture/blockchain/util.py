import base64
from algosdk import mnemonic
from algosdk.atomic_transaction_composer import *
from algosdk.abi import Method, Contract
from algosdk.encoding import decode_address, encode_address


def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response["result"])


def get_private_key_from_mnemonic(mn):
    private_key = mnemonic.to_private_key(mn)
    return private_key


def format_state(state):
    formatted = {}
    for item in state:
        key = item["key"]
        value = item["value"]
        formatted_key = base64.b64decode(key).decode("utf-8")
        if value["type"] == 1:
            formatted_value = base64.b64decode(value["bytes"])
            if formatted_key == 'authorityAddress':
                formatted[formatted_key] = encode_address(formatted_value)
            else:
                formatted[formatted_key] = formatted_value
        else:
            formatted[formatted_key] = value["uint"]
    return formatted


def read_global_state(client, app_id):
    app = client.application_info(app_id)
    global_state = (
        app["params"]["global-state"] if "global-state" in app["params"] else []
    )
    return format_state(global_state)


def read_local_state(client, addr, app_id) :
    results = client.account_info(addr)
    local_state = results['apps-local-state'][0]
    for index in local_state:
        if local_state[index] == app_id :
            local = local_state['key-value']
    return format_state(local)


def get_method(name: str, js: str) -> Method:
    c = Contract.from_json(js)
    for m in c.methods:
        if m.name == name:
            return m
    raise Exception("No method with the name {}".format(name))
