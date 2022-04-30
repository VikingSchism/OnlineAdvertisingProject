import numpy as np
import matplotlib.pyplot as plt
import json

vals = []

for i in range(1,7):
    watts = []
    with open('watts_' + str(i) + 'thread.out') as f:
        lines = f.readlines()

        for j in range(len(lines)):
            #        if i % 2 == 0:
            #           amps.append(json.loads(lines[i][48:])['value'])
            #        else:
            watts.append(json.loads(lines[j][48:])['value'])
    vals.append(watts)

fig, (axs1, axs2) = plt.subplots(2,3)
for i in range(3):
    axs1[i].plot(np.arange(len(vals[i])), np.array(vals[i]))
    axs1[i].plot(np.arange(len(vals[i])), np.repeat(np.average(vals[i]), len(vals[i])))
    axs2[i].plot(np.arange(len(vals[2+i])), np.array(vals[2+i]))
plt.show()
