import numpy as np
import matplotlib.pyplot as plt
import json

watts = []
vals = []

with open("watts_20thread.out") as f:
    lines = f.readlines()
    for j in range(len(lines)):
        val = json.loads(lines[j][48:])['value']
        if val != 0:
            watts.append(val)
    vals.append(watts)

watts = []
with open("watts_7thread.out") as f:
    lines = f.readlines()
    for j in range(len(lines)):
        val = json.loads(lines[j][48:])['value']
        if val != 0:
            watts.append(val)
    vals.append(watts)

fig, ax = plt.subplots()
bp = ax.boxplot(vals, showmeans=True)
ax.set_ylabel("Power (W)")
plt.xticks([1,2], ["20 DSPs", "7 DSPs"])
ax.set_title("20 DSPs connected")
plt.show()
