import os
from dotenv import load_dotenv
from pathlib import Path
from web3 import Web3
import json 
import binascii
import sys

#define path to load data from .env file 
dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)

#define web3 RPC provider
rpc_provider = os.getenv('RPC_PROVIDER')
w3 =  Web3(Web3.HTTPProvider(rpc_provider))

#define own adress
wallet_address = '0x090f395Bd24E8Ba7e0A2730ADB387d5Be9428Af5'
wallet_address = Web3.toChecksumAddress(wallet_address)
private_key = os.getenv('PRIVATE_KEY')

#define contract
contract_address = '0x715514960eac1ef8b06b2d3779dcfaa29c6e61ba'
contract_address = Web3.toChecksumAddress(contract_address)
ABI = json.loads('[{"inputs":[{"internalType":"string","name":"_greeting","type":"string"}],"name":"setGreeting","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"greet","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"greeting","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]')
contract = w3.eth.contract(contract_address, abi=ABI)


#change file hash 
def writeHashToBC(filehash):
    try:
        nonce = w3.eth.getTransactionCount(wallet_address)
        transaction = contract.functions.setGreeting(filehash).buildTransaction({
        'chainId': 4,
        'gas': 1400000,
        'gasPrice': w3.toWei('160', 'gwei'),
        'nonce': nonce,
        'from': wallet_address
        }) 
        signed_txn = w3.eth.account.signTransaction(transaction, private_key=private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    except Exception as e:
        sys.exit("An error occurred " + str(e))

    #tx_hash is in ASCII binary 
    return binascii.hexlify(tx_hash)


def getFileHash():
    try:
        ethFilehash = contract.functions.greet().call()
    except Exception as e:
        sys.exit("An error occurred " + str(e))

    return ethFilehash
