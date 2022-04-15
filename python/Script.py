import os
from dotenv import load_dotenv
from pathlib import Path
from web3 import Web3
import datetime
import json 

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

# define contract
contract_address = '0x715514960eac1ef8b06b2d3779dcfaa29c6e61ba'
contract_address = Web3.toChecksumAddress(contract_address)
ABI = json.loads('[{"inputs":[{"internalType":"string","name":"_greeting","type":"string"}],"name":"setGreeting","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"greet","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"greeting","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]')
contract = w3.eth.contract(contract_address, abi=ABI)


def getName():
    callgreeter = contract.functions.greeting().call()
    return callgreeter

#change greeting 
def changeName(greeting):
    nonce = w3.eth.getTransactionCount(wallet_address)
    transaction = contract.functions.setGreeting(greeting).buildTransaction({
    'chainId': 4,
    'gas': 1400000,
    'gasPrice': w3.toWei('160', 'gwei'),
    'nonce': nonce,
    'from': wallet_address
    }) 
    signed_txn = w3.eth.account.signTransaction(transaction, private_key=private_key)
    w3.eth.sendRawTransaction(signed_txn.rawTransaction)


#print(getName())
#changeName("WHATS UP")


#read file return hash 
def hashFile():
    f = open("./file.txt", "r")
    return hash(f.read)


#print hash to file 
def printhash():
    with open("./file.txt", "a") as f:
        f.write("\n ")
        f.write("\n ---------------------------------")
        f.write("\n Date: " + str(datetime.datetime.now()))
        f.write("\n Integrity Hash: " + str(hashFile()))
        f.write("\n ---------------------------------")
            
printhash()