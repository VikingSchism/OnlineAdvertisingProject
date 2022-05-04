import numpy as np
import matplotlib.pyplot as plt
import json

vals = []

for i in range(1,8):
    watts = []
    with open('watts_' + str(i) + 'thread.out') as f:
        lines = f.readlines()

        for j in range(len(lines)):
            #        if i % 2 == 0:
            #           amps.append(json.loads(lines[i][48:])['value'])
            #        else:
            val = json.loads(lines[j][48:])['value']
            if val != 0:
                watts.append(val)
        print('watts_' + str(i) + 'thread.out')
        print(np.mean(watts))
    vals.append(watts)

fig, ax = plt.subplots()
bp = ax.boxplot(vals, showmeans=True)
ax.set_xlabel("DSPs connected")
ax.set_ylabel("Power (W)")
ax.set_title("Connected DSPs vs idle power consumption")

mins = [round(item.get_ydata()[0],3) for item in bp['caps']][::2]
maxs = [round(item.get_ydata()[0],3) for item in bp['caps']][1::2]

ranges = list(map(lambda x, y: x - y, maxs, mins))
print(ranges)

means = [round(item.get_ydata()[0],3) for item in bp['means']]
print(means)

    
#for i in range(3):
#    axs1[i].plot(np.arange(len(vals[i])), np.array(vals[i]))
#    axs1[i].plot(np.arange(len(vals[i])), np.repeat(np.average(vals[i]), len(vals[i])))
#    axs2[i].plot(np.arange(len(vals[2+i])), np.array(vals[2+i]))
plt.show()
