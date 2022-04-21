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
contract_address = '0xFf8cCbe6FF79a0EC9b4A85a84124bA4f282FF147'
contract_address = Web3.toChecksumAddress(contract_address)
ABI = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"_adress","type":"address"},{"internalType":"string","name":"name","type":"string"}],"name":"addCollaborator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_adress","type":"address"}],"name":"deleteCollaborator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getHash","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getLastModifyed","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"hash","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lastModifyedBy","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_hash","type":"string"}],"name":"setHash","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_newOwner","type":"address"}],"name":"setOwner","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
contract = w3.eth.contract(contract_address, abi=ABI)


#change file hash 
def writeHashToBC(filehash):
    try:
        nonce = w3.eth.getTransactionCount(wallet_address)
        transaction = contract.functions.setHash(filehash).buildTransaction({
        'chainId': 4,
        'gas': 1400000,
        'gasPrice': w3.toWei('160', 'gwei'),
        'nonce': nonce,
        'from': wallet_address
        }) 
        signed_txn = w3.eth.account.signTransaction(transaction, private_key=private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    except Exception as e:
        #Exit because error cant be transfered 
        sys.exit("An error occurred " + str(e))

    #tx_hash is in ASCII binary 
    return binascii.hexlify(tx_hash)


#get file hash
def getFileHash():
    try:
        ethFilehash = contract.functions.getHash().call()
    except Exception as e:
        #Exit because error cant be transfered 
        sys.exit("An error occurred " + str(e))

    return ethFilehash

def getLastModifyed():
    try:
        lastModifyedBy = contract.functions.getLastModifyed().call()
    except Exception as e:
        #Exit because error cant be transfered 
        sys.exit("An error occurred " + str(e))

    return lastModifyedBy


def setAdress(adress, name):
    try:
        nonce = w3.eth.getTransactionCount(wallet_address)
        transaction = contract.functions.addCollaborator(adress, name).buildTransaction({
        'chainId': 4,
        'gas': 1400000,
        'gasPrice': w3.toWei('160', 'gwei'),
        'nonce': nonce,
        'from': wallet_address
        }) 
        signed_txn = w3.eth.account.signTransaction(transaction, private_key=private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    except Exception as e:
        #Exit because error cant be transfered 
        sys.exit("An error occurred " + str(e))

    #tx_hash is in ASCII binary 
    return binascii.hexlify(tx_hash)


def deleteAdress(adress):
    try:
        nonce = w3.eth.getTransactionCount(wallet_address)
        transaction = contract.functions.deleteCollaborator(adress).buildTransaction({
        'chainId': 4,
        'gas': 1400000,
        'gasPrice': w3.toWei('160', 'gwei'),
        'nonce': nonce,
        'from': wallet_address
        }) 
        signed_txn = w3.eth.account.signTransaction(transaction, private_key=private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    except Exception as e:
        #Exit because error cant be transfered 
        sys.exit("An error occurred " + str(e))

    #tx_hash is in ASCII binary 
    return binascii.hexlify(tx_hash)