import socket
import time
import sys

s = socket.socket()
host = sys.argv[1]
port = 12345
try:
    s.connect((host,port))
    s.sendall(b'site')
    data = s.recv(1024)
    print(data.decode())
    time.sleep(0.05)
    tic = time.perf_counter()
    s.sendall(b'AD PLS')
    data = s.recv(2048)
    print(data.decode())
    toc = time.perf_counter()
    print(f"Time taken: {toc - tic}")
    s.close()
except:
    print("Cannot connect to server")
