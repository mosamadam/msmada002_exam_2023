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
        print(f"mnemonic of Account: {account_index.get(i)}: {mnemonic.from_private_key(private_key)}")

number_accounts = 2
create_account(number_accounts)

#save address and mnemonic of each account to be used at a later stage
add_A = "WLWW3J2Z3UM3CGOFJEFPPDANGIIIOMNT73GZK6SQJZM5IAXZCETY7BNRA4"
mn_A = "fog despair jaguar royal diamond green glove stone chalk wear play liquid report rose hazard scrub lens tag quick crunch bread tower giant about drum"

add_B = "DVZ5EJZUHCIKXQ5SLQ5OFR2BZG67AGE3FHD2KJGCWB7PHVVTZR7ELB6WPU"
mn_B = "scene cloth neglect talk friend similar price announce poem acquire lab bracket rack agent tuition guide then domain victory venture whisper buzz obey absent churn"

number_accounts = 3
create_account(number_accounts)

add_1 =  "E24S5DUAJ444ZSY6IJMOADHZTWMNADLGJC2IQRGQPZV2FI4KE3CUZAHRZI"
mn_1 = "trophy drop public vacuum inhale giraffe deny alter tuition amount else canvas account cute satisfy naive ticket tilt brown seek doll pride scissors about hundred"

add_2 = "CSOCGH2R3GSKF3RADIEHD2FKO6QXGDQ5ZNG6E3RER435DGQWKGGZGDBWUM"
mn_2 = "review drive first skull harsh wife dizzy assault rotate waste like decorate final video once senior city perfect sadness base urban blanket indoor absent dizzy"

add_3 = "U3A65UTRIPJC7B4CKAD4N5KZHAI6PIJWL5E56IZ3OSZKRVW6BCI53L7EPI"
mn_3 = "receive achieve nephew reason mutual unknown where promote air clerk stone welcome unfold action lion note struggle lecture paddle crime soccer child tissue above link"