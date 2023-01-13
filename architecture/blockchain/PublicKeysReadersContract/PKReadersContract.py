from algosdk.atomic_transaction_composer import *
from pyteal import *
from algosdk import account, mnemonic

creator_mnemonic = "infant flag husband illness gentle palace eye tilt large reopen current purity enemy depart couch moment gate transfer address diamond vital between unlock able cave"
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "p8IwM35NPv3nRf0LLEquJ5tmpOtcC4he7KKnJ3wE"
headers = {
    "X-API-Key": algod_token,
}

from pyteal import *

reader_address = Bytes("readerAddress")
pk_reader_ipfs_link = Bytes("pk_ipfs_link")


def getRouter():
    router = Router(
        "StoreReaderPublicKeyContract",
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
            App.globalPut(reader_address, Global.zero_address()),
            App.globalPut(pk_reader_ipfs_link, Int(0)),
        )

    @router.method(no_op=CallConfig.CALL)
    def on_save(reader: abi.Account, ipfs_link: abi.String) -> Expr:
        return Seq(
            App.globalPut(reader_address, reader.address()),
            App.globalPut(pk_reader_ipfs_link, ipfs_link.get()),
        )

    return router
    