import os
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import FuncFormatter, MultipleLocator
from scipy import integrate

# total time
base_time = 4.0
pause_time = 1.5
total_time = base_time + pause_time

# fig
fig, ax = plt.subplots()

# plots
plot_0 = None
plot_25 = None
plot_50 = None
plot_75 = None
plot_100 = None
plot_125 = None
plot_150 = None
plot_175 = None
plot_200 = None

def set_title(title):
    ax.set_title("{0}".format(title))

def set_lim(x_lim_begin, x_lim_end, y_lim_begin, y_lim_end):
    ax.set_xlim(x_lim_begin, x_lim_end)
    ax.set_ylim(y_lim_begin, y_lim_end)

def init_plot(name):
    x_data = []
    y_data = []

    plot = ax.plot([], [], label=name)[0]
    plot.set_data(x_data, y_data)

    return plot

def plot_append_value(p, x_value, y_value):
    x_data = p.get_xdata()
    y_data = p.get_ydata()

    x_data.append(x_value)
    y_data.append(y_value) 

    p.set_data(x_data, y_data)

def animation_plot(plot_data_table, contrast, i):
    x_value = i 
    y_value = math.pow(x_value / 0.18, contrast) * 0.18

    plot_append_value(plot_data_table, x_value, y_value)

def init_figure():
    # title
    set_title("f(x, c) = pow(x/0.18, c) * 0.18")

    # lim
    set_lim(0.0, 1.0, 0.0, 4.0)

    # global
    global plot_0
    global plot_25
    global plot_50
    global plot_75
    global plot_100
    global plot_125
    global plot_150
    global plot_175

    # init
    plot_0 = init_plot("0.0")
    plot_25 = init_plot("0.25")
    plot_50 = init_plot("0.5")
    plot_75 = init_plot("0.75")
    plot_100 = init_plot("1.0")
    plot_125 = init_plot("1.25")
    plot_150 = init_plot("1.5")
    plot_175 = init_plot("1.75")

    # show legend
    ax.legend()    

def animation_frame(i):
    if i > base_time:
        return

    t = i / 4.0
    
    animation_plot(plot_0,   0.0,  t)
    animation_plot(plot_25,  0.25, t)
    animation_plot(plot_50,  0.5,  t)
    animation_plot(plot_75,  0.75, t)
    animation_plot(plot_100, 1.0,  t)
    animation_plot(plot_125, 1.25, t)
    animation_plot(plot_150, 1.5,  t)
    animation_plot(plot_175, 1.75, t)

# delta time
play_speed = 0.5
dt = 0.02 * play_speed
            
# figure size (pixels->inches) 
# https://matplotlib.org/devdocs/gallery/subplots_axes_and_figures/figure_size_units.html
px = 1/plt.rcParams["figure.dpi"]
fig_width = float(960) * px
fig_height = float(960) * px

# clear
fig, ax = plt.subplots(figsize=(fig_width, fig_height))

# show grid
ax.grid()

# animation
anim = animation.FuncAnimation(fig, init_func=init_figure, func=animation_frame, frames=np.arange(0, total_time, dt), interval=dt * 1000 / play_speed)

# save to gif
anim.save("contrast.gif", writer='pillow')

# save last frame to png
fig.savefig("contrast.png")