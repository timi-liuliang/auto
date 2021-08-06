import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import xml.etree.ElementTree as ET

# total time
tt = 10.0

# delta time
dt = 0.02

# line datas
x_data = []
y_data = []

fig, ax = plt.subplots()

ax.set_xlim(0, 105)
ax.set_ylim(0, 12)
ax.set_title("Title")

plots = []
plots.append(ax.plot(0, 0, label="Line 0")[0])

ax.legend()
#ax.grid()

def load_plots(file_path):
    tree = ET.parse("plots.xml")
    plots_node = tree.getroot()

    

    return


def animation_frame(i):
    if(i*10 <100):
        x_data.append(i * 10)
        y_data.append(math.sin(i) + 6.0) 

    plots[0].set_xdata(x_data)
    plots[0].set_ydata(y_data)

    #ax.scatter(i*10, i*5.0)

anim = animation.FuncAnimation(fig, init_func=load_plots, func=animation_frame, frames=np.arange(0, tt, dt), interval=dt * 1000)
anim.save('result.gif', writer='pillow')