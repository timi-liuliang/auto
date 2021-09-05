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
plots = []

def set_title(title):
    ax.set_title("{0}".format(title))

def set_lim(x_lim_begin, x_lim_end, y_lim_begin, y_lim_end):
    ax.set_xlim(x_lim_begin, x_lim_end)
    ax.set_ylim(y_lim_begin, y_lim_end)

def init_figure():
    # title
    set_title("Clothoid")

    # lim
    set_lim(-4.0, 12.0, -2.0, 2.0)

    plot = ax.plot([], [], label="C(x)")[0]

    x_data = []
    y_data = []
    plot.set_data(x_data, y_data)

    plots.append(plot)

    # show legend
    ax.legend()    

def f(x):
    return math.cos(x*x)      

def animation_frame(i):
    if i > base_time:
        return

    idx = 0

    x_value = i * math.pi
    y_value, error = integrate.quad(f, 0, x_value)

    x_data = plots[idx].get_xdata()
    y_data = plots[idx].get_ydata()

    x_data.append(x_value)
    y_data.append(y_value) 

    plots[idx].set_data(x_data, y_data)  

# delta time
play_speed = 0.5
dt = 0.02 * play_speed
            
# figure size (pixels->inches) 
# https://matplotlib.org/devdocs/gallery/subplots_axes_and_figures/figure_size_units.html
px = 1/plt.rcParams["figure.dpi"]
fig_width = float(960) * px
fig_height = float(240) * px

# clear
fig, ax = plt.subplots(figsize=(fig_width, fig_height))
ax.xaxis.set_major_formatter(FuncFormatter(lambda val,pos: '{:.0g}$\pi$'.format(val/np.pi) if val !=0 else '0'))
ax.xaxis.set_major_locator(MultipleLocator(base=np.pi))

# show grid
ax.grid()

# animation
anim = animation.FuncAnimation(fig, init_func=init_figure, func=animation_frame, frames=np.arange(0, total_time, dt), interval=dt * 1000 / play_speed)

# save to gif
anim.save("clothoid.gif", writer='pillow')

# save last frame to png
fig.savefig("clothoid.png")