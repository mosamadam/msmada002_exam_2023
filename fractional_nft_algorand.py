from algosdk import account, mnemonic
from algosdk import transaction
from algosdk.v2client import algod
import math


#connect to PureStake node
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = ""
headers = {
   "X-API-Key": "rNM1J80x888yEcKfQ9m7p3BNXANkrIk53xdJmX6Y",
}
algod_client = algod.AlgodClient(algod_token, algod_address, headers)

#function to extract asset balance
def gettokenbalance(account_address,token_ID):
    account_info = algod_client.account_info(account_address)
    for a in account_info["assets"] : 
        if (a['asset-id'] == token_ID):
            return (a['amount'])

#funding account: an account created to fund accounts geneerated
fund_add = "C7N262ZEWW6CUX36LPUPW4B7TAP52IF3RGXZ4DZR6DWOZVIDGOY6TYTOUQ"
fund_pk = "MS2JrxXuB8jX9ohxvOn2OVRvDNnxdQuSCvqb79cY684X269rJLW8Kl9+W+j7cD+YH90gu4mvng8x8Ozs1QMzsQ=="

#create accounts required for question
accounts = {}
def create_account(no_account):
    for i in range(no_account):
        private_key, address = account.generate_account()
        print(f"address of Account_{i}: {address}")
        accounts[f"account_{i}"] = {"private_key": private_key, "address": address}
    return accounts

#specify the number of accounts required for question (includes NFT account): 4 accounts would be needed for question
no_account = int(input("How many account should be created? \n"))
account_all = create_account(no_account)

#fund all accounts from funding account
for i in range(no_account):
    add_rec = account_all[f"account_{i}"]["address"]
    params = algod_client.suggested_params()

    unsigned_txn = transaction.PaymentTxn(
        sender=fund_add,
        sp=params,
        receiver=add_rec,
        amt=500000,
        note=b"",
    )
    signed_txn = unsigned_txn.sign(fund_pk)
    txid = algod_client.send_transaction(signed_txn)
    txn_result = transaction.wait_for_confirmation(algod_client, txid, 4)

#assume first account (Account_0) is the account which creates the nft
creator_account = account_all["account_0"]

#specify the number of decimals (to be used to determine the fraction of NFT)
decimal = int(input("Specify the number of decimals \n"))
amount = pow(10, decimal)

#specify default gas fee
sp = algod_client.suggested_params()

#create TCURAZ NFT with quantity = 1
txn = transaction.AssetConfigTxn(
    sender=creator_account["address"],
    sp=sp,
    default_frozen=False,
    unit_name="TCURAZ",
    asset_name="TCURAZ Token",
    manager=creator_account["address"],
    reserve=creator_account["address"],
    freeze=creator_account["address"],
    clawback=creator_account["address"],
    total=amount,
    decimals=decimal,
)

# Sign with secret key of creator
stxn = txn.sign(creator_account["private_key"])
# Send the transaction to the network and retrieve the txid.
txid = algod_client.send_transaction(stxn)

results = transaction.wait_for_confirmation(algod_client, txid, 4)

#print asset number
created_asset = results["asset-index"]
print(f"Asset ID created: {created_asset}")


#add fractional nft to each account (account 1 to n)
for i in range(1, no_account):
    reciever_add = account_all[f"account_{i}"]["address"]
    reciever_pk = account_all[f"account_{i}"]["private_key"]

    balance = gettokenbalance(creator_account["address"], created_asset)

    #determine if correct fraction has been input 
    while True:
        frac_input = input(f"How much would you like to transfer to Account_{i}? (Value within {decimal} decimal places and within the bounds {1/amount} < x < {balance/amount})\n")
        try:
            frac = float(frac_input)
            if frac <= 1/amount or frac >= balance/amount:
                print("Value entered is out of bounds.")
            elif len(str(frac).split(".")[1]) > decimal:
                print(f"Please enter a value to only {decimal} decimal places")
            else:
                break 
        except ValueError:
            print("Invalid input. Please enter a valid value.")

    frac = int(frac*amount)

    optin_txn = transaction.AssetOptInTxn(
            sender=reciever_add, sp=sp, index=created_asset
        )

    signedOptInTxn = optin_txn.sign(reciever_pk)
    txid = algod_client.send_transaction(signedOptInTxn)
    print(f"Sent opt in transaction with txid: {txid}")

    # Wait for the transaction to be confirmed
    results = transaction.wait_for_confirmation(algod_client, txid, 4)

    # Create transfer transaction
    xfer_txn = transaction.AssetTransferTxn(
        sender=creator_account["address"],
        sp=sp,
        receiver=reciever_add,
        amt=frac,
        index=created_asset,
    )
    signed_xfer_txn = xfer_txn.sign(creator_account["private_key"])
    txid = algod_client.send_transaction(signed_xfer_txn)
    print(f"Sent transfer transaction with txid: {txid}")

    results = transaction.wait_for_confirmation(algod_client, txid, 4)

#check if accounts_1 to account_n hold the token

for i in range(1, no_account):

    account_i = account_all[f"account_{i}"]["address"]
    asset_check = gettokenbalance(account_i, created_asset)

    if asset_check != "none":
        print(f"The address: {account_i} \nHolds the following amount of asset with ID: {created_asset} \n {asset_check/amount} TCURAZ")
    else:
        print(f"The address: {account_i} \nDoes not hold asset with ID: {created_asset}")




