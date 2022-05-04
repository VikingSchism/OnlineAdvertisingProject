import socket
import os
from threading import *
from queue import Queue
from ast import literal_eval
import sys

dspQueue = Queue()
workQueue = Queue()
aucQueue = Queue()

s = socket.socket()
host = sys.argv[1]
port = 12345
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    s.bind((host,port))
except socket.error as e:
    print(str(e))

    
    
print('I\'m listening...')
s.listen(5)

# Control logic for the DSP connections in parallel
def handle_dsp(connection):
    global workQueue
    global aucQueue
    global dspQueue
    done = False
    while True:
        if not done and workQueue.qsize() > 0:
            print("waiting on work")
            msg = workQueue.get()
            connection.sendall(msg)
            data = connection.recv(2048)
            if not data:
                break
            tup = literal_eval(data.decode())
            aucQueue.put(tup)
            done = True
            print("work done")
        if workQueue.empty() and done:
            done = False
    dspQueue.get()
    connection.close()
    
#Control logic for the site connection in parallel
def handle_ssp(connection):
    global workQueue
    global dspQueue
    global aucQueue
    while True:
        print("Waiting on data")
        msg = connection.recv(2048)
        print("Data received: " + msg.decode())
        if not msg:
            break
        
        workerAmount = dspQueue.qsize()
        for i in range(workerAmount):
            workQueue.put(msg)
        while not aucQueue.qsize() == 0:
            # wait
            pass
        aucList = []
        for i in range(workerAmount):
            auc = aucQueue.get()
            aucList.append(auc)
        res = max(aucList)
        connection.sendall(f"{res[0]}: {res[1]}".encode())
    connection.close()
        
            
#Determine if incoming connection is a DSP or SSP
def handle_client(connection):
    global dspQueue
    connection.sendall(str.encode('Server is working'))
    data = connection.recv(2048)
    print(data)
    if data.decode() == 'DSP':
        print('DSP connected')
        dsp = Thread(target=handle_dsp, args=(connection, ))
        dspQueue.put(dsp)
        dsp.start()
    else:
        print('Non DSP')
        ssp = Thread(target=handle_ssp, args=(connection, ))
        ssp.start()

        
while True:
    c, addr = s.accept()
    print("Got connection from", addr)
    handle_client(c)
s.close()

