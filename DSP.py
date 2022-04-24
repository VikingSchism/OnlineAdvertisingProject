import socket
import csv
import sys

def readDict(dictName):
    with open(dictName, newline='') as f:
        reader = csv.reader(f)
        return {rows[0]:int(rows[1]) for rows in reader}

def doAuction(bidDict):
    maxBid = max(zip(bidDict.values(), bidDict.keys()))
    return maxBid

def connectToSSP(bidDict):
    s = socket.socket()
    host = sys.argv[1]
    port = 12345
    try:
        s.connect((host,port))
        s.sendall(b'DSP')
        while True:
            incoming = s.recv(1024).decode()
            if not incoming:
                break
            print("Got a message: " + incoming)
            if incoming != 'Server is working':
                aucRes = doAuction(bidDict)
                reply = str(aucRes)
                s.sendall(reply.encode())
        s.close()
    except ConnectionRefusedError:
        print("Cannot connect to server")


dictName = sys.argv[2]
try:
    bidDict = readDict(dictName)
except FileNotFoundError:
    print("There doesn't seem to be a file with that name.")
    quit()

connectToSSP(bidDict)
