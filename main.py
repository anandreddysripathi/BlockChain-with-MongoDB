import json
import ast
import hashlib

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

    # #getter method
    # def displayBlock(self):
    #     print("displaying block data: "+self._data)
    #     print(" previousHash: "+self._previousHash)
    #     print "nonce :",self._nonce
    #     print("sender :"+self._sender)
    #     print("receipent:"+self._recipient)
    #     print "difficulty level :" ,self._difficulty

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
    global allBlocks
    if len(allBlocks):
        print("creating block")
        data = raw_input("enter the data")
        blockdiff = difficulty[len(difficulty)-1]
        prevHash = chainHash
        sender = raw_input("\n enter sender :")
        receiver = raw_input("\n enter receiver:")
    else:
        print("creating genesis block")
        data = "Genesis Block"
        prevHash = ""
        blockdiff = 2
        sender = ""
        receiver = ""
    gB = Block()
    gB.setBlockValues(data, prevHash, 1, sender, receiver, blockdiff)
    blockData = gB.hashBlock()
    blockHashValue = blockData["chainHash"]
    blockData.pop("chainHash")
    blockData.pop("difficulty")
    chainHash = blockHashValue
    allBlocks2.append(json.dumps(blockData))
    allBlocks.append(str(blockData))
    if not len(difficulty)==len(allBlocks):
        difficulty.append(blockdiff)

#importing blockchain JSON from a text file
def importBlockChain():
    global allBlocks,chainHash,difficulty
    inputFile=raw_input("enter the txt file of the JSON file")
    with open(inputFile) as f:
        json_data = json.load(f)
    chainHash=json_data["chainHash"]
    difficulty=json_data["difficulty"]
    allBlocks=json_data["blockchain"]
    print "the block chain data is \n"
    print json.dumps(allBlocks)
    verifyBlockchain()

#adding a block to blockchain
def addBlock():
    createBlock()

#verifying the block
def verifyBlockchain():
    print("verifying.....")

    i=0
    corrupted=False
    while i<len(allBlocks)-1:
        takeBlockData = allBlocks[i]
        result = ast.literal_eval(takeBlockData)
        data = result["data"]
        # print "printing data " , data
        prevHash = result["previousHash"]
        sender = result["sender"]
        receiver = result["recipient"]
        blockdiff = difficulty[i]
        gb = Block()
        gb.setBlockValues(data, prevHash, 1, sender, receiver, blockdiff)
        blockData = gb.hashBlock()
        currentChainHash = blockData["chainHash"]
        nextBlock = ast.literal_eval(allBlocks[i + 1])
        if not nextBlock["previousHash"]== currentChainHash:
            print("blockchain error occured:\n at block {x}".format(x=i + 1))
            corrupted=True
            break
        i+=1
    if corrupted:
        print "corrupted"
    else:
        print "blockchain is verified"

    viewBlockchain()
#display the blockchain
def viewBlockchain():
    # printBlocks(allBlocks)
    print "difficulty ", difficulty
    print "chian Hash is ",chainHash

#corrupt the blockchain
def corruptBlock():
    a = int(input("enter the block you want to corrupt: "))
    data = raw_input("enter new data")
    # converting string dictionary to dictionary
    newBlockData = ast.literal_eval(allBlocks[a - 1])
    newBlockData["data"] = data
    allBlocks[a-1]=str(newBlockData)
    allBlocks2[a-1]=str(newBlockData)

def fixCorruption():
    print("fix corruption working")
    i=0
    while i<len(allBlocks):
        takeBlockData = allBlocks[i]
        result = ast.literal_eval(takeBlockData)
        data = result["data"]
        prevHash = result["previousHash"]
        sender = result["sender"]
        receiver = result["recipient"]
        blockdiff = difficulty[i]
        gb2 = Block()
        gb2.setBlockValues(data, prevHash, 1, sender, receiver, blockdiff)
        blockData = gb2.hashBlock()
        currentChainHash = blockData["chainHash"]
        chainHash=currentChainHash
        blockData.pop("chainHash")
        blockData.pop("difficulty")
        allBlocks[i]=str(blockData)
        if i<len(allBlocks)-1:
            # assigning current block hash to next block's prevhash
            nextBlockData = ast.literal_eval(allBlocks[i + 1])
            nextBlockData["previousHash"] = currentChainHash
            allBlocks[i+1]=str(nextBlockData)
        i+=1

    verifyBlockchain()
    print "fixed corruption"

#exportig the current block chain to text file
def exportBlockchain():
    print("exporting...........")
    jsonDict["chainHash"] = chainHash
    jsonDict["difficulty"] = difficulty
    jsonDict["blockchain"] = allBlocks2
    # exporting the blockchain
    with open('blockchain.txt', 'w') as json_file:
        json.dump(jsonDict, json_file)
    print "Exported"

#importing a JSON blockchain from text file and checking if it matches the current blockchain
def loadAndCompare():
    print("loadAndCompare working")
    global allBlocks, chainHash, difficulty
    inputFile = raw_input("enter the txt file of the JSON file")
    with open(inputFile) as f:
        json_data = json.load(f)
    chainHash2 = json_data["chainHash"]
    if chainHash2==chainHash:
        print "the blockchains are same"
    else:
        print "blockchains are not same"

#adjusting the difficulty
def adjustDiffculty():
    print("adjust difficulty working")
    tempDiff=int(input("enter new difficulty maximum of 7"))
    difficulty.append(tempDiff)

#terminate from program
def terminateProgram():
    exit("exiting")

requestInput = "------------------------------------------------\n1:Add a block\t\t\t6:export blockchain \n" \
               "2:Verify blockchain\t\t7:import and compare with current blockchain \n" \
               "3:View blockchain\t\t8:adjust blockchain difficulty \n" \
               "4:corrupt a block\t\t9:terminate program\n" \
               "5:fix corruption"

prompt = int(input("0:Create a new blockchain 1:import a blockchain\n"))
if not prompt:
    createBlock()
else:
    importBlockChain()

# printing all the Blocks
def printBlocks(blocks):
    print "The Block Chain as of now with ({x} blocks) is:\n".format(x=len(allBlocks))
    for i in allBlocks:
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
        7: loadAndCompare,
        8: adjustDiffculty,
        9: terminateProgram
    }
    switcher[response]()