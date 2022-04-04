import socket
import os
from _thread import *

s = socket.socket()
host = '192.168.1.145'
port = 12345
ThreadCount = 0
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    s.bind((host,port))
except socket.error as e:
    print(str(e))

print('I\'m listening...')
s.listen(5)

signal = False

def handle_client(connection):
    global signal
    dsp = False
    
    connection.sendall(str.encode('Server is working:'))
    data = connection.recv(2048)
    if data.decode() == 'DSP':
        print('DSP connected')
        lock = True
        dsp = True
    else:
        print('Non DSP')
        lock = False
    while True:
        if signal and lock and dsp:
            msg = 'advert pls'
            connection.sendall(msg.encode())
            data = connection.recv(2048)
            if not data:
                break
            print(data.decode())
            lock = False
        if not signal and not lock and dsp:
            lock = True
        elif not lock and not dsp:
            data = connection.recv(2048)
            print(data.decode())
            if not data:
                print("Signal is now false")
                signal = False
                break
            if data.decode() == 'AD PLS':
                signal = True
                print("Signal is here")
    connection.close()


while True:
    c, addr = s.accept()
    print("Got connection from", addr)
    start_new_thread(handle_client, (c, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
s.close()

