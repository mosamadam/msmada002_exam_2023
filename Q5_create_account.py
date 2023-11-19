from algosdk import account, mnemonic
from algosdk import transaction

#create two accounts account_A and account_B

#create dectionary with account A and B


def create_account(number):
    account_index = {0: "A", 1: "B", 2:"C"}

    for i in range(number):

        #create account
        private_key, address = account.generate_account()

        # print and save the address and mnemonic for each acount 
        print(f"address of Account: {account_index.get(i)}: {address}")
        print(f"private key of Account: {account_index.get(i)}: {private_key}")
        print(f"mnemonic of Account: {account_index.get(i)}: {mnemonic.from_private_key(private_key)}")

number_accounts = 2
create_account(number_accounts)

#save address and mnemonic of each account to be used at a later stage
add_A = "WLWW3J2Z3UM3CGOFJEFPPDANGIIIOMNT73GZK6SQJZM5IAXZCETY7BNRA4"
mn_A = "fog despair jaguar royal diamond green glove stone chalk wear play liquid report rose hazard scrub lens tag quick crunch bread tower giant about drum"

add_B = "DVZ5EJZUHCIKXQ5SLQ5OFR2BZG67AGE3FHD2KJGCWB7PHVVTZR7ELB6WPU"
mn_B = "scene cloth neglect talk friend similar price announce poem acquire lab bracket rack agent tuition guide then domain victory venture whisper buzz obey absent churn"
