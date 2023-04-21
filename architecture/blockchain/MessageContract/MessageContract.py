from algosdk.atomic_transaction_composer import *
from pyteal import *
from algosdk import account, mnemonic
from decouple import config


creator_mnemonic = config('PASSPHRASE_CREATOR')
algod_address = config('ALGOD_ADDRESS')
algod_token = config('ALGOD_TOKEN')
headers = {
   "X-API-Key": algod_token,
}


from pyteal import *


messageID = Bytes("msg_id")
IPFSLink = Bytes("ipfs_link")


def getRouter():
    router = Router(
        "StorageMessageContract",
        BareCallActions(
            # On create only, just approve
            # no_op=OnCompleteAction.create_only(Approve()),
            # Always let creator update/delete but only by the creator of this contract
            # update_application=OnCompleteAction.always(Reject()),
            delete_application=OnCompleteAction.call_only(Approve()),
        ),
    )


    @router.method(no_op=CallConfig.CREATE)
    def create_app():
        return Seq(
            App.globalPut(messageID, Int(0)),
            App.globalPut(IPFSLink, Int(0)),
        )

    @router.method(no_op=CallConfig.CALL)
    def on_save(message_id: abi.String, ipfs_link: abi.String) -> Expr:
        return Seq(
            App.globalPut(messageID, message_id.get()),
            App.globalPut(IPFSLink, ipfs_link.get()),
        )

    return router
