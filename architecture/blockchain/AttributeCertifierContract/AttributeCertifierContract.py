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


processID = Bytes("process_id")
IPFSLink = Bytes("ipfs_link")


def getRouter():
    router = Router(
        "StorageAttributesContract",
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
            App.globalPut(processID, Int(0)),
            App.globalPut(IPFSLink, Int(0)),
        )

    @router.method(no_op=CallConfig.CALL)
    def on_save(process_id: abi.String, ipfs_link: abi.String) -> Expr:
        return Seq(
            App.globalPut(processID, process_id.get()),
            App.globalPut(IPFSLink, ipfs_link.get()),
        )

    return router
