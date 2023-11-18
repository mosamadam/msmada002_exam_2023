from algosdk import account, mnemonic
from algosdk import transaction
from algosdk.v2client import algod
from Q5_create_account import add_B, mn_B, add_1, mn_1

#connect to PureStake node
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = ""
headers = {
   "X-API-Key": "rNM1J80x888yEcKfQ9m7p3BNXANkrIk53xdJmX6Y",
}
algod_client = algod.AlgodClient(algod_token, algod_address, headers)

#get private key from mnemonic of account B
pk_1 = mnemonic.to_private_key(mn_1)

#specify default gas fee
sp = algod_client.suggested_params()

decimal = 3
amount = pow(10, decimal)
fraction = amount/decimal
fraction_1 = round(fraction)

if fraction_1==fraction:
    fraction_2 = fraction_1
elif fraction_1>fraction:
    fraction_2 = fraction_1 -1
else:
    fraction_2 = fraction_1 + 1

print(fraction_1, fraction_2)

#create UCTZAR asset with quantity = 1000
txn = transaction.AssetConfigTxn(
    sender=add_1,
    sp=sp,
    default_frozen=False,
    unit_name="TCURAZ",
    asset_name="TCURAZ Token",
    manager=add_1,
    reserve=add_1,
    freeze=add_1,
    clawback=add_1,
    total=amount,
    decimals=decimal,
)

# Sign with secret key of creator
stxn = txn.sign(pk_1)
# Send the transaction to the network and retrieve the txid.
txid = algod_client.send_transaction(stxn)

results = transaction.wait_for_confirmation(algod_client, txid, 4)

#print asset number
created_asset = results["asset-index"]
print(f"Asset ID created: {created_asset}")

#save asset_ID

