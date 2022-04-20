from distutils.log import error
from sys import argv
import datetime
import hashlib
from black import err
import typer
from blockchainService import writeHashToBC, getFileHash, getLastModifyed
from os.path import exists


#read file return hash 
def hashFile(filename):
    hasher = hashlib.new("sha256")
    fileLength = checkFilelenght(filename)
  
    try:
        f = open(filename, "rb")
        content = f.readlines()
        content = str(content[0 : fileLength]).encode('utf-8')
        hasher.update(content)
        return hasher.hexdigest()
    except EnvironmentError as err:
        print("An error occured " + str(err))



#print hash to file 
def verifyFile(filename):
    if exists(filename):
        filehash = str(hashFile(filename))            
        
        #write hash to blockchain
        tx_hash = "0x" + str(writeHashToBC(filehash))[2:-1]
        
        #write hash to file 
        try:
            with open(filename, "a") as f:      
                f.write("\n ")
                f.write("\n ---------------------------------")
                f.write("\n Filename: " + filename)
                f.write("\n Date: " + str(datetime.datetime.now()))
                f.write("\n Last changes by: " + getLastModifyed())
                f.write("\n Integrity Hash: " + filehash)
                f.write("\n TX: " + "https://rinkeby.etherscan.io/tx/" + tx_hash)
                f.write("\n ---------------------------------")
        except EnvironmentError as err:
            print("An error occured " + str(err))
    else: 
        print("File not Found")



def checkFilelenght(filename):
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.find('---- FILE ENDS HERE ----') != -1:
                    return lines.index(line)
                 
            num_lines = len(lines)
            try:
                with open(filename, "a") as f:
                    f.write("\n ---- FILE ENDS HERE ----")
                return num_lines

            except EnvironmentError as err:
                print("An error occured " + err)

    except EnvironmentError as err:
        print("An error occured " + str(err))


def checkFile(filename):
    if exists(filename):
        if getFileHash() == hashFile(filename):
            print("#################################")
            print("Date: " + str(datetime.datetime.now()))
            print("The file " +  filename + " is integer")
            print("Last changes by:" + getLastModifyed())
        else:
            print("#################################")
            print("Date: " + str(datetime.datetime.now()))
            print("The file " +  filename + " is not integer")
    else:
        print("File not found")

#print hash to file and blockchain
#verifyFile("file.txt")

#check file integrity 
checkFile("file.txt")


