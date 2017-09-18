from hashlib import sha256
import logging
import datetime

REPLACE_CODE, NO_REPLACE_CODE = (0, 1)


def calculateHash(index, previousHash, timestamp, data):
    string = str(index) + str(previousHash) + str(timestamp) + str(data)
    return sha256(bytes(string, 'utf-8')).hexdigest()


class Block:
    def __init__(self,
                 index,
                 previousHash,
                 timestamp,
                 data,
                 hash):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.data = data
        self.hash = str(hash)

    def calcultateSelfHash(self):
        return calculateHash(self.index, self.previousHash, self.timestamp,
                             self.data)


def generateNextBlock(blockData):
    previousBlock = getLatestBlock()
    nextIndex = previousBlock.index + 1
    nextTimestamp = datetime.datetime.now()
    nextHash = calculateHash(nextIndex, previousBlock.hash, nextTimestamp,
                             blockData)
    return Block(nextIndex, previousBlock.hash, nextTimestamp,
                 blockData, nextHash)


def getGenesisBlock():
    return Block(0, "0", '0',
                 "Genesis Block!",
                 calculateHash(0, '0', '0', "Genesis Block!")
                 )


blockchain = [getGenesisBlock()]


def isValidNewBlock(newBlock, previousBlock):
    if (previousBlock.index != newBlock.index - 1):
        logging.warning('invalid index')
        return False
    elif previousBlock.hash != newBlock.previousHash:
        logging.warning('invalid previousHash')
        return False
    elif newBlock.calcultateSelfHash() != newBlock.hash:
        logging.warning('invalid hash')
        return False

    return True


def getLatestBlock():
    return blockchain[-1]


def addBlock(newBlock):
    if isValidNewBlock(newBlock, getLatestBlock()):
        blockchain.append(newBlock)


def isChainValid(chain):
    if chain[0] != getGenesisBlock():
        return False

    for b1, b2 in zip(chain[:-1], chain[1:]):
        if not isValidNewBlock(b2, b1):
            return False

    return True


def replaceChain(newBlocks):
    global blockchain
    if isChainValid(newBlocks) and len(newBlocks) > len(blockchain):
        logging.warning('New blockchain is valid, replacing current chain...')
        blockchain = newBlocks
        return REPLACE_CODE
    else:
        logging.warning('Recieved block is invalid!')
        return NO_REPLACE_CODE
