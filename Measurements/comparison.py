import numpy as np
import matplotlib.pyplot as plt
import sys
import json

dsps = sys.argv[1]
vals = []


with open('watts_' + dsps + '_ssp.out') as f:
    watts = []
    for line in f:
        val = json.loads(line[48:])['value']
        watts.append(val)
    vals.append(watts)
with open('watts_' + dsps + 'thread.out') as f:
    for line in f:
        val = json.loads(line[48:])['value']
        watts.append(val)
    vals.append(watts)
fig, ax = plt.subplots()
ax.boxplot(vals)
plt.show()
