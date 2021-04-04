import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def set_figure_area(
    num_row, num_col, size, facecolor='white', legend_font_color='black', 
    legend_face='white', spine_color='black', tick_color='black', 
    axis_label_color='black'
    ): 


    fig= plt.figure(figsize=size)
    axis = []
    for i in range(num_row*num_col): 
        axis.append(plt.subplot(num_row, num_col, i+1))
    fig.set_facecolor(facecolor) # fig outside background color
    for ax in axis: 
        ax.set_facecolor(facecolor) # fig inside background color
        legend = ax.legend(facecolor=legend_face, edgecolor=legend_face)
        for text in legend.get_texts(): 
            text.set_color(legend_font_color) # set legend and color
 
        ax.spines['bottom'].set_color(spine_color)
        ax.spines['left'].set_color(spine_color)
        ax.spines['top'].set_color(spine_color)
        ax.spines['right'].set_color(spine_color) # axis color
        ax.tick_params(axis='x', colors=tick_color)
        ax.tick_params(axis='y', colors=tick_color) # tick color
        ax.xaxis.label.set_color(axis_label_color)
        ax.yaxis.label.set_color(axis_label_color) # label color

    return fig, axis

