from algosdk import account, mnemonic
from algosdk import transaction
from algosdk.v2client import algod
from Q5_create_account import add_B, mn_B

#connect to PureStake node
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = ""
headers = {
   "X-API-Key": "rNM1J80x888yEcKfQ9m7p3BNXANkrIk53xdJmX6Y",
}
algod_client = algod.AlgodClient(algod_token, algod_address, headers)

#get private key from mnemonic of account B
pk_B = mnemonic.to_private_key(mn_B)

#specify default gas fee
sp = algod_client.suggested_params()

#create UCTZAR asset with quantity = 1000
txn = transaction.AssetConfigTxn(
    sender=add_B,
    sp=sp,
    default_frozen=False,
    unit_name="UCTZAR",
    asset_name="UCTZAR Token",
    manager=add_B,
    reserve=add_B,
    freeze=add_B,
    clawback=add_B,
    total=1000,
    decimals=0,
)

# Sign with secret key of creator
stxn = txn.sign(pk_B)
# Send the transaction to the network and retrieve the txid.
txid = algod_client.send_transaction(stxn)

results = transaction.wait_for_confirmation(algod_client, txid, 4)

#print asset number
created_asset = results["asset-index"]
print(f"Asset ID created: {created_asset}")

#save asset_ID
asset_id = "480396491"