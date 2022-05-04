import sys
import os
import threading

ip = sys.argv[1]

def connect_dsp(ip):
    os.system("python3 DSP.py " + ip + " google.csv")


for i in range(20):
    dsp = threading.Thread(target=connect_dsp, args=(ip,))
    dsp.start()
