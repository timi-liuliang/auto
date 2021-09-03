import os
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import xml.etree.ElementTree as ET
import argparse

# working dir
workingdir = os.getcwd() + '/temp/'

# target extension
target_ext = ".gif"

# file
figure_file = ""
figure_node = None

# fig
fig, ax = plt.subplots()

# plots
plots = []

def set_title():
    title = figure_node.attrib["title"]
    play_speed = float(figure_node.attrib["play_speed"])
    ax.set_title("{0} (Play Speed : {1}x)".format(title, play_speed))

def set_lim():
    x_lim_begin = float(figure_node.attrib["x_lim_begin"])
    x_lim_end = float(figure_node.attrib["x_lim_end"])
    y_lim_begin = float(figure_node.attrib["y_lim_begin"])
    y_lim_end = float(figure_node.attrib["y_lim_end"])
    
    ax.set_xlim(x_lim_begin, x_lim_end)
    ax.set_ylim(y_lim_begin, y_lim_end)

def load_figure():
    # title
    set_title()

    # lim
    set_lim()

    for plot_node in figure_node:
        if plot_node.attrib["type"] == "Line":
            label_name = plot_node.attrib["label"]
            plot = ax.plot([], [], label=label_name)[0]

            x_data = []
            y_data = []
            plot.set_data(x_data, y_data)

            plots.append(plot)
        elif plot_node.attrib["type"] == "NavSpline":
            label_name = plot_node.attrib["label"]
            plot = ax.plot([], [], label=label_name)[0]

            x_data = []
            y_data = []

            for index, key_node in enumerate(plot_node):
                key_value = key_node.attrib["value"].split(" ")
                x_data.append(float(key_value[0]))
                y_data.append(float(key_value[1]))

            plot.set_data(x_data, y_data)

            plots.append(plot)

    # show legend
    ax.legend()          

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

    return False, float(0.0), float(0.0)

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

# get files sort by datetime
def getfiles(dirpath):
    a = [s for s in os.listdir(dirpath)]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    a.reverse()

    return a
    
# parse target ext
parser = argparse.ArgumentParser(description='figure save type', conflict_handler='resolve')
parser.add_argument('-save_type', help='saving type', default='.gif')
args = parser.parse_args()

target_ext = args.save_type

for file in getfiles(workingdir):
    if file.endswith(".xml"):
        figure_file = os.path.join(workingdir, file)
        gif_file = os.path.join(workingdir, os.path.splitext(figure_file)[0] + target_ext)
        if not os.path.exists(gif_file):
            # load
            figure_node = ET.parse(figure_file).getroot()

            # total time
            tt = float(figure_node.attrib["total_time"])

            # delta time
            play_speed = float(figure_node.attrib["play_speed"])
            dt = 0.02 * play_speed
            
            # figure size (pixels->inches) 
            # https://matplotlib.org/devdocs/gallery/subplots_axes_and_figures/figure_size_units.html
            px = 1/plt.rcParams["figure.dpi"]
            fig_size = figure_node.attrib["size"].split(" ")
            fig_width = float(fig_size[0]) * px
            fig_height = float(fig_size[1]) * px

            # clear
            fig, ax = plt.subplots(figsize=(fig_width, fig_height))

            plots = []

            # grid
            show_grid = int(figure_node.attrib["grid"])
            if show_grid > 0 :
                ax.grid()

            # animation
            anim = animation.FuncAnimation(fig, init_func=load_figure, func=animation_frame, frames=np.arange(0, tt, dt), interval=dt * 1000 / play_speed)

            # save to gif
            if target_ext == ".mp4" :
                anim.save(gif_file, writer="ffmpeg")
            else:
                anim.save(gif_file, writer='pillow')