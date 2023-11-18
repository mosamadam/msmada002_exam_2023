from algosdk import account, mnemonic
from algosdk import transaction
from algosdk.v2client import algod
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
    AccountTransactionSigner,
    TransactionWithSigner,
)
from typing import Dict, Any
import sys

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
        

if __name__ == "__main__":

    #user B input -------------------------------------------------------------------
    mn_B = input('User B: Enter you Mnemonic?\n')
    #determine private key and address from mnemonic
    pk_B = mnemonic.to_private_key(mn_B)
    add_B = account.address_from_private_key(pk_B)

    asset_id = input('User B: Enter your asset ID?\n')
    sell_q = input('Would you like to sell your asset? y/n \n')
    #terminate programme if user does not agree to transaction
    if sell_q.lower() != 'y':
        sys.exit("User B did not agree to the terms.")

    price_q = input('How much would you like to sell and for what price?\n')
    price_q = [int(num.strip()) for num in price_q.split()]
    #print(price_q)

    #include price data in dictionary
    price_deal = {"token": price_q[0], "price":price_q[1]}

    #terminate programme if user does not have enough tokens for transaction
    if gettokenbalance(add_B, int(asset_id)) < price_deal["token"]:
        sys.exit("Your token balance is insufficient")


    #user A input -------------------------------------------------------------------
    mn_A = input('User A: Enter you Mnemonic?\n')
    #determine private key and address from mnemonic
    pk_A = mnemonic.to_private_key(mn_A)
    add_A = account.address_from_private_key(pk_A)

    buy_q = input(f'Do you agree to purchase the asset with the following details? y/n \n Asset ID: {asset_id} \n Quantity: {price_deal["token"]} \n Price: {price_deal["price"]} microAlgos \n')
    account_info: Dict[str, Any] = algod_client.account_info(add_A)
    add_A_balance = account_info.get('amount')
    #terminate programme if user does not agree to transaction
    if buy_q.lower() != 'y':
        sys.exit("User A did not agree to the terms.")
    elif add_A_balance < price_deal["price"]:
        sys.exit("User A has insufficient funds.")

    #process atomic transaction, first opt-in, then with asset transfer-------------------------

    #optin------------------------------------------------------------------------
    sp = algod_client.suggested_params()
    # Create opt-in transaction
    optin_txn = transaction.AssetOptInTxn(
        sender=add_A, sp=sp, index=asset_id
    )
    signed_optin_txn = optin_txn.sign(pk_A)
    txid = algod_client.send_transaction(signed_optin_txn)
    print(f"Sent opt in transaction with txid: {txid}")

    # Wait for the transaction to be confirmed
    results = transaction.wait_for_confirmation(algod_client, txid, 4)
    print(f"Result confirmed in round: {results['confirmed-round']}")

    #initiate atomic transfer signatures------------------------------------------------------------------------------
    atc = AtomicTransactionComposer()
    # Create signer object
    signer_A = AccountTransactionSigner(pk_A)
    signer_B = AccountTransactionSigner(pk_B)

    #Create transfer of asset------------------------------------------------------------------------
    xfer_txn = transaction.AssetTransferTxn(
        sender=add_B,
        sp=sp,
        receiver=add_A,
        amt=price_deal["token"],
        index=asset_id,
    )

    # Construct TransactionWithSigner
    tws_B = TransactionWithSigner(xfer_txn, signer_B)

    # Pass TransactionWithSigner to ATC
    atc.add_transaction(tws_B)

    #create Algos transaction------------------------------------------------------------------------
    unsigned_txn = transaction.PaymentTxn(
    sender=add_A,
    sp=sp,
    receiver=add_B,
    amt=price_deal["price"],
    note=b"",
    )

    # Construct TransactionWithSigner
    tws_A = TransactionWithSigner(unsigned_txn, signer_A)

    # Pass TransactionWithSigner to ATC
    atc.add_transaction(tws_A)

    #execute atomic transaction------------------------------------------------------------------------
    try:
        result = atc.execute(algod_client, 4)
        print(f"The transaction was successfull. Please refer to the transaction ID's below \n {result.tx_ids}")
    except Exception as err:
        print(err)



        





