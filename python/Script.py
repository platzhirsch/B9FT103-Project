from sys import argv
import datetime
import hashlib
import typer
from blockchainService import writeHashToBC
from blockchainService import getFileHash


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
     else: 
        num_lines = sum(1 for line in open('./file.txt'))
        with open("file.txt", "a") as f:
                f.write("---- FILE ENDS HERE ----")
        return num_lines
        

def checkFileIntegrity():
    if getFileHash() == hashFile():
        print("The file is integer")
    else:
        print("The file is not integer")

checkFileIntegrity()