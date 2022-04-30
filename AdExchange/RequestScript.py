import os
import sys

ip = sys.argv[1]

for i in range(100):
    os.system("python3 SSPRequest.py " + ip)
