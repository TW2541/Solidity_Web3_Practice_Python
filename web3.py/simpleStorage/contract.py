import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# get contract address
with open("./web3.py/simpleStorage/contract_address", "r") as file:
    contract_address = file.read()

# get contract abi
with open("./web3.py/simpleStorage/abi.json", "r") as file:
    abi = json.load(file)

# for connecting to testnet
w3 = Web3(Web3.HTTPProvider("http://localhost:7545"))
chain_id = 1337
my_address = os.environ.get("MY_ADDRESS")
private_key = os.environ.get("PRIVATE_KEY")

# initial contract variable
simple_storage = w3.eth.contract(address=contract_address, abi=abi)
print()
print("Contract : %s" % contract_address)

"""
Contract Functions :
1. store(uint256 number) : Store number
2. retrieve() : Get stored number
3. addPerson(string name,uint256 number) : add person name and num to array

Contract Values :
1. people[uint256] : call person from array
2. nameToFavoriteNumber(string name) : search name to get number
"""

# select functions to interact with
function_dict = {
    1: "store",
    2: "retrieve",
    3: "addPerson",
    4: "people",
    5: "nameToFavoriteNumber"
}
for func_key in function_dict:
    print(func_key, function_dict.get(func_key))
selected_function = int(input("Select function to execute : "))
print()
# check method (call or transact)
isTransact = False

if function_dict.get(selected_function) == "store":
    number = input("Input number : ")
    print("Building transaction function => store")
    transaction = simple_storage.functions.store(int(number)).buildTransaction(
        {"chainId": chain_id, "from": my_address, "nonce": w3.eth.getTransactionCount(my_address)})
    isTransact = True

elif function_dict.get(selected_function) == "retrieve":
    print(simple_storage.functions.retrieve().call())

elif function_dict.get(selected_function) == "addPerson":
    name, number = input("Input name and number : ").split()
    print("Building transaction function => addPerson")
    transaction = simple_storage.functions.addPerson(name, int(number)).buildTransaction(
        {"chainId": chain_id, "from": my_address, "nonce": w3.eth.getTransactionCount(my_address)})
    isTransact = True

elif function_dict.get(selected_function) == "people":
    index = input("Input index : ")
    print(simple_storage.functions.people(int(index)).call())

elif function_dict.get(selected_function) == "nameToFavoriteNumber":
    name = input("Input name : ")
    print(simple_storage.functions.nameToFavoriteNumber(name).call())


if isTransact:
    print("Signing Transaction with address : %s" % my_address)
    signed_transaction = w3.eth.account.sign_transaction(
        transaction, private_key=private_key)
    print("Sending Transaction...")
    transaction_hash = w3.eth.send_raw_transaction(
        signed_transaction.rawTransaction)
    print("Completing %s..." % w3.toHex(transaction_hash))
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
    print("transaction is completed")

print()
