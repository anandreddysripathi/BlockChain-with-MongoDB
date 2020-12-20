import pymongo
from pymongo import MongoClient
import json
import datetime
import sys
import json
import ast
import unicodedata

import hashlib

#connecting to the  MongoDB Atlas
client = MongoClient("mongodb+srv://anand:anand98@mycluster.y3ecg.mongodb.net/Mycluster?retryWrites=true&w=majority")
db = client['blockChain']
collection = db["transactions"]

#checking if connection is successful by adding and deleting a document.
try:
    collection.insert_one({"sample":"document"})
    collection.delete_many({})
except pymongo.errors.OperationFailure:
    print("mongoDB connection failed")
    print("redirecting to the original Blockchain execution")
    execfile('main.py')
    sys.exit()

print("connection with mongoDB is successful")

jsonDict = {}
allBlocks = []
chainHash = ""
difficulty = []
allBlocks2 = []


class Block:

    def __init__(self, data=None, previousHash=None, nonce=None, sender=None, recipient=None, difficulty=None):
        self._data = data
        self._previousHash = previousHash
        self._nonce = nonce
        self._sender = sender
        self._recipient = recipient
        self._difficulty = difficulty

    # setter method to assign values to block's private variables
    def setBlockValues(self, data, prevHash, nonce, sender, receiver, difficulty):
        self._data = data
        self._previousHash = prevHash
        self._nonce = nonce
        self._sender = sender
        self._recipient = receiver
        self._difficulty = difficulty


    # this the block
    def hashBlock(self):
        def hashTheBlockData(string):
            string = str.encode(str(string))
            hashed_string = hashlib.sha256(string).hexdigest()
            return hashed_string
        #looping till nonce values matches with the difficulty level
        while True:
            hashed_string = hashTheBlockData(
                self._data + self._previousHash + str(self._nonce) + self._sender + self._recipient)
            if hashed_string[:self._difficulty] == "0" * self._difficulty:
                break
            self._nonce += 1
        blockDict = {
            "data": self._data,
            "previousHash": self._previousHash,
            "difficulty": self._difficulty,
            "nonce": self._nonce,
            "sender": self._sender,
            "recipient": self._recipient,
            "chainHash": hashed_string
        }
        return blockDict

#creating a block
def createBlock():
    global chainHash
    print("creating block")
    blockDifficulty=int(raw_input("enter block's difficulty"))
    data=raw_input("enter block data")
    blockSender=raw_input("enter sender")
    blockReceiver=raw_input("enter receiver")
    if collection.count_documents({}):
        previousHash=chainHash
    else:
        previousHash=""
    gB=Block()
    gB.setBlockValues(data,previousHash,1,blockSender,blockReceiver,blockDifficulty)
    blockData=gB.hashBlock()
    chainHash=blockData["chainHash"]
    temp=blockData["data"]
    blockData["data"]=int(temp)
    blockData.pop("chainHash")
    blockData.pop("nonce")
    print blockData
    blockData['_id']= collection.count_documents({}) + 1
    collection.insert_one(blockData)
    print chainHash

#adding a block to blockchain
def addBlock():
    createBlock()

#verifying the block
def verifyBlockchain():
    print("verifying.....")

    index=1
    corrupted=False
    for document in collection.find({}):
        result = document
        nextdocument=collection.find_one({"_id":index+1})
        # print nextdocument
        nextdocumentPrevHash=nextdocument["previousHash"].encode('ascii','ignore')
        data = result["data"]
        prevHash = result["previousHash"]
        sender = result["sender"]
        receiver = result["recipient"]
        blockdiff = result["difficulty"]
        gb = Block()
        gb.setBlockValues(data, prevHash, 1, sender, receiver, blockdiff)
        blockData = gb.hashBlock()
        currentChainHash = blockData["chainHash"]
        if not nextdocumentPrevHash== currentChainHash:
            print "chain hash is", currentChainHash
            print "next doc prev hash is", nextdocumentPrevHash
            print("blockchain error occured:\n at block {x}".format(x=index))
            corrupted=True
            break
        index+=1
        if index==collection.count_documents({}):
            break
    if corrupted:
        print "corrupted"
    else:
        print "blockchain is verified"

    # viewBlockchain()
#display the blockchain
def viewBlockchain():
    if not collection.count_documents({}):
        print("empty blockchain , add transacitions")
    else:
        for document in collection.find({}):
            print document
        a=collection.find()
        print("\n \n")
        print(a)
#corrupt the blockchain
def corruptBlock():
    blocknumber = int(input("enter the block you want to corrupt: "))
    data = raw_input("enter new data")
    collection.update_one({"_id":blocknumber},{"$set": { "data": data } })

def fixCorruption():
    index = 1
    # corrupted = False
    for document in collection.find({}):
        result = document
        nextdocument = collection.find_one({"_id": index + 1})
        # print nextdocument
        nextdocumentPrevHash = nextdocument["previousHash"].encode('ascii', 'ignore')
        data = result["data"]
        prevHash = result["previousHash"]
        sender = result["sender"]
        receiver = result["recipient"]
        blockdiff = result["difficulty"]
        gb = Block()
        gb.setBlockValues(data, prevHash, 1, sender, receiver, blockdiff)
        blockData = gb.hashBlock()
        currentChainHash = blockData["chainHash"]
        if not nextdocumentPrevHash == currentChainHash:
            print("before updating, next block's prev hash is ")
            print nextdocumentPrevHash
            collection.update({"_id":index+1},{"$set":{"previousHash":currentChainHash}})
            print("updated the next block's prev hash in mongodb ")
            corrnextdoc=collection.find_one({"_id":index+1})
            print(corrnextdoc["previousHash"].encode('ascii','ignore'))
        index += 1
        if index == collection.count_documents({}):
            break

#exportig the current block chain to text file
def exportBlockchain():
    print("exporting...........")
    jsonDict=list(collection.find({}))
    # exporting the blockchain
    with open('mongoblockchain.txt', 'w') as json_file:
        json.dump(jsonDict, json_file)
    print "Exported"

#terminate from program
def terminateProgram():
    exit("exiting")

requestInput = "------------------------------------------------\n1:Add a block\t\t\t6:export blockchain \n" \
               "2:Verify blockchain\t\t7:display CS572 student \n" \
               "3:View blockchain\t\t8:run query \n" \
               "4:corrupt a block\t\t9:terminate program\n" \
               "5:fix corruption"

# printing all the Blocks
def printBlocks(blocks):
    print "The Block Chain as of now with ({x} blocks) is:\n".format(x=len(allBlocks))
    for i in allBlocks:
        print i
def displayHI():
    print("Hi I'm a CS 572 student ")


def executeTheQueries():
    query1Question="return the transactions whose data value is greater than 100,receipient is not vivek and  sorted in descending order of data  "
    query1=collection.find({
        "data": {"$gt": 100},
        "$nor": [{"recipient": "vivek"}]
    }).sort([("data", -1)])
    print(query1Question)
    for i in query1:
        print i
    query2Question="return the number of transaction returned by each sender"
    query2=collection.aggregate([{
        "$group" : {"_id" : "$sender",
        "num_transactions" : {"$sum" : 1}}
    }])
    print(query2Question)
    for i in query2:
        print i

while True:
    print(requestInput)
    response = int(input("\nEnter a selection: "))
    print(response)
    switcher = {
        1: addBlock,
        2: verifyBlockchain,
        3: viewBlockchain,
        4: corruptBlock,
        5: fixCorruption,
        6: exportBlockchain,
        7: displayHI,
        8: executeTheQueries,
        9: terminateProgram
    }
    switcher[response]()

