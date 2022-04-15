import os
from sys import argv
import binascii
from dotenv import load_dotenv
from pathlib import Path
from web3 import Web3
import datetime
import json 
import hashlib
import typer


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

    #tx_hash is in ASCII binary 
    return binascii.hexlify(tx_hash)



#read file return hash 
def hashFile():
    hasher = hashlib.new("sha256")
    fileLength = checkFilelenght()
    if type(fileLength) == int:
        f = open("./file.txt", "rb")
        content = f.readlines()
        content = str(content[0 : fileLength]).encode('utf-8')
        hasher.update(content)
        return hasher.hexdigest()
    else:
        print("File is empty")
     


#print hash to file 
def printhash():

    filehash = str(hashFile())

    if checkFilelenght() == False:
            with open("file.txt", "a") as f:
                f.write("---- FILE ENDS HERE ----")
    
    #write hash to blockchain
    tx_hash = "0x" + str(writeHashToBC(filehash))[2:-1]
    
    #write hash to file 
    with open('file.txt', "a") as f:      
        f.write("\n ")
        f.write("\n ---------------------------------")
        f.write("\n Date: " + str(datetime.datetime.now()))
        f.write("\n Integrity Hash: " + filehash)
        f.write("\n TX: " + "https://rinkeby.etherscan.io/tx/" + tx_hash)
        f.write("\n ---------------------------------")
   


def checkFilelenght():
    with open("./file.txt", 'r') as f:
     lines = f.readlines()
     for line in lines:
         if line.find('---- FILE ENDS HERE ----') != -1:
            return lines.index(line)
     else: return False
          


def getFileHash():
    ethFilehash = contract.functions.greet().call()
    return ethFilehash


def checkFileIntegrity():
    if getFileHash() == hashFile():
        print("The file is integer")
    else:
        print("The file is not integer")




app = typer.Typer()

@app.command()
def checkTxtFileIntegrity():
    checkFileIntegrity()


@app.command()
def SaveFileHash():
    printhash()

if __name__ == "__main__":
    app()

#Hash file and write to blockchain 
#printhash()

#Check file integrity 


