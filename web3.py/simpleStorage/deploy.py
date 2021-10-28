from solcx import compile_standard, install_solc
from web3 import Web3
from dotenv import load_dotenv
import json
import os

load_dotenv()

with open("./solidity/contract/SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile Solidity
install_solc("0.8.7")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "SimpleStorage.sol": {"content": simple_storage_file}
        },
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.7",
)

with open("./web3.py/simpleStorage/compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
with open("./web3.py/simpleStorage/bytecode.json", "w") as file:
    json.dump(bytecode, file)

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
with open("./web3.py/simpleStorage/abi.json", "w") as file:
    json.dump(abi, file)

# for connecting to testnet
w3 = Web3(Web3.HTTPProvider("http://localhost:7545"))
chain_id = 1337
my_address = os.environ.get("MY_ADDRESS")
private_key = os.environ.get("PRIVATE_KEY")

# create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# build a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce})

# sign a transaction
signed_transaction = w3.eth.account.sign_transaction(
    transaction, private_key=private_key)

# send a signed transaction
transaction_hash = w3.eth.send_raw_transaction(
    signed_transaction.rawTransaction)

# wait for complete transaction
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
print("Contract %s has been created" % transaction_receipt.contractAddress)
# get contract address
with open("./web3.py/simpleStorage/contract_address", "w") as file:
    file.write(transaction_receipt.contractAddress)
