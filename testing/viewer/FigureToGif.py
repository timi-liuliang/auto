import os
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import xml.etree.ElementTree as ET

# file
figure_file = "figure_2021.08.06-10.08.55.xml"

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

def load_plots():
    tree = ET.parse(figure_file)
    figure_node = tree.getroot()

    print(figure_node)

def animation_frame(i):
    if(i*10 <100):
        x_data.append(i * 10)
        y_data.append(math.sin(i) + 6.0) 

    plots[0].set_xdata(x_data)
    plots[0].set_ydata(y_data)

    #ax.scatter(i*10, i*5.0)

anim = animation.FuncAnimation(fig, init_func=load_plots, func=animation_frame, frames=np.arange(0, tt, dt), interval=dt * 1000)

# save to gif
gif_file = os.path.splitext(figure_file)[0] + ".gif"
anim.save(gif_file, writer='pillow')