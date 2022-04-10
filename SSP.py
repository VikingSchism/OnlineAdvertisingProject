import socket
import os
from threading import *
from queue import Queue

dspQueue = Queue()
workQueue = Queue()

s = socket.socket()
host = '192.168.1.145'
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
    done = False
    while True:
        if not done and workQueue.qsize() > 0:
            print("waiting on work")
            msg = workQueue.get()
            connection.sendall(msg)
            data = connection.recv(2048)
            if not data:
                break
            print(data.decode())
            done = True
            print("work done")
        if workQueue.empty():
            print("time for new work")
            done = False
    connection.close()
    
#Control logic for the site connection in parallel
def handle_site(connection):
    global workQueue
    global dspQueue
    while True:
        print("Waiting on data")
        msg = connection.recv(2048)
        print("Data received: " + msg.decode())
        if not msg:
            break
        
        workerAmount = dspQueue.qsize()
        for i in range(workerAmount):
            workQueue.put(msg)
        
            
#Determine if incoming connection is a DSP or client
def handle_client(connection):
    dsp = False
    global dspQueue
    
    connection.sendall(str.encode('Server is working:'))
    data = connection.recv(2048)
    if data.decode() == 'DSP':
        print('DSP connected')
        dsp = Thread(target=handle_dsp, args=(connection, ))
        dspQueue.put(dsp)
        dsp.start()
    else:
        print('Non DSP')
        site = Thread(target=handle_site, args=(connection, ))
        site.start()


while True:
    c, addr = s.accept()
    print("Got connection from", addr)
    handle_client(c)
s.close()

