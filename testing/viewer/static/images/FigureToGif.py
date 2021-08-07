import os
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import xml.etree.ElementTree as ET

# file
figure_file = ""
figure_node = None

# total time
tt = 50.0

# delta time
dt = 0.02

# fig
fig, ax = plt.subplots()

# plots
plots = []

def set_time_range():
    tt = float(figure_node.attrib["total_time"])

def set_lim():
    x_lim_begin = float(figure_node.attrib["x_lim_begin"])
    x_lim_end = float(figure_node.attrib["x_lim_end"])
    y_lim_begin = float(figure_node.attrib["y_lim_begin"])
    y_lim_end = float(figure_node.attrib["y_lim_end"])
    
    ax.set_xlim(x_lim_begin, x_lim_end)
    ax.set_ylim(y_lim_begin, y_lim_end)

def load_figure():
    # time range
    set_time_range()

    # lim
    set_lim()

    for plot_node in figure_node:
        if plot_node.attrib["type"] == "Line":
            plot = ax.plot([], [], label=plot_node.attrib["label"])[0]

            x_data = []
            y_data = []
            plot.set_data(x_data, y_data)

            plots.append(plot)
            

def line_key_interpolation(now, plot_node):
    for index, key_node in enumerate(plot_node):
        next_time = time = float(key_node.attrib["time"])
        next_value = pre_value = key_node.attrib["value"].split(" ")
        ratio = 1.0

        if index < len(plot_node) - 1:
            next_key_node = plot_node[index+1]
            next_time = float(next_key_node.attrib["time"])
            next_value =  next_key_node.attrib["value"].split(" ")
            ratio = (now - time) / (next_time - time)

        if now>=time and now <=next_time :
            now_x_value = float(pre_value[0]) + ratio * (float(next_value[0]) - float(pre_value[0]))
            now_y_value = float(pre_value[1]) + ratio * (float(next_value[1]) - float(pre_value[1]))

            return True, now_x_value, now_y_value

    return False, float(pre_value[0]), float(pre_value[0])

def animation_frame(i):
    for idx, plot_node in enumerate(figure_node):
        if plot_node.attrib["type"] == "Line":
            succeed, x_value, y_value = line_key_interpolation(i, plot_node)
            if succeed :
                x_data = plots[idx].get_xdata()
                y_data = plots[idx].get_ydata()

                x_data.append(x_value)
                y_data.append(y_value) 

                plots[idx].set_data(x_data, y_data)


for file in os.listdir(os.getcwd()):
    if file.endswith(".xml"):
        figure_file = file
        gif_file = os.path.splitext(figure_file)[0] + ".gif"
        if not os.path.exists(gif_file):
            # load
            figure_node = ET.parse(figure_file).getroot()
            
            # clear
            fig, ax = plt.subplots()
            ax.set_title("Car Rerversing")

            plots = []

            # animation
            anim = animation.FuncAnimation(fig, init_func=load_figure, func=animation_frame, frames=np.arange(0, tt, dt), interval=dt * 1000)

            # save to gif
            anim.save(gif_file, writer='pillow')