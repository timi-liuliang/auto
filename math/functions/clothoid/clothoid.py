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
plot_cos = None
plot_sin = None
plot_cx = None
plot_sx = None
plot_spiral = None

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

def animation_cos(i):
    x_value = (i - base_time / 2.0) * math.pi 
    y_value = math.cos(x_value * x_value)

    plot_append_value(plot_cos, x_value, y_value)

def animation_sin(i):
    x_value = (i - base_time / 2.0) * math.pi 
    y_value = math.sin(x_value * x_value)

    plot_append_value(plot_sin, x_value, y_value)

def fc(x):
    return math.cos(x*x)

def animation_cx(i):
    x_value = (i - base_time / 2.0) * math.pi 
    y_value, error = integrate.quad(fc, 0, x_value)

    plot_append_value(plot_cx, x_value, y_value)   

def fs(x):
    return math.sin(x*x)

def animation_sx(i):
    x_value = (i - base_time / 2.0) * math.pi
    y_value, error = integrate.quad(fs, 0, x_value)

    plot_append_value(plot_sx, x_value, y_value)

def animation_spiral(i):
    x_value = (i - base_time / 2.0) * math.pi
    y_value, error = integrate.quad(fc, 0, x_value)
    z_value, error = integrate.quad(fs, 0, x_value)

    plot_append_value(plot_spiral, y_value, z_value)

def init_figure():
    # title
    set_title("Clothoid")

    # lim
    set_lim(-8.0, 8.0, -2.0, 2.0)

    # global
    global plot_cos
    global plot_sin
    global plot_cx
    global plot_sx
    global plot_spiral

    # init
    plot_cos = init_plot("Cos(x^2)")
    plot_sin = init_plot("Sin(x^2)")
    plot_cx  = init_plot("C(x)")
    plot_sx  = init_plot("S(x)")
    plot_spiral = init_plot("Spiral")

    # show legend
    ax.legend()    

def animation_frame(i):
    if i > base_time:
        return

    animation_cos(i)
    animation_sin(i)
    animation_cx(i)
    animation_sx(i)
    animation_spiral(i)

# delta time
play_speed = 0.5
dt = 0.02 * play_speed
            
# figure size (pixels->inches) 
# https://matplotlib.org/devdocs/gallery/subplots_axes_and_figures/figure_size_units.html
px = 1/plt.rcParams["figure.dpi"]
fig_width = float(960*2.0) * px
fig_height = float(240*2.0) * px

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