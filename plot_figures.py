'''
This file contains class for dynamic monitor
'''
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import set_figure_area

class DisplayAll(): 
    '''
    a class of monitor display all data, usually create automatically with 
    class DynamicMonitor
    '''
    def __init__(self, ax, line_type='-o'): 
        '''
        axis: axis list from plt.subplot
        line_type: string
        '''
        self.line_type = line_type
        self.ax = ax
        self.x_label = 'X'
        self.y_label = 'Y'
        self.line = []
        self.y_lim = ()
    
    def set_y_lim(self, y_lim): 
        '''
        y_lim: tuple of float
        '''
        self.y_lim = y_lim

    def set_label(self, label): 
        '''
        label: tuple of strings, (x_label, y_label)
        '''
        self.x_label = label[0]
        self.y_label = label[1]

    def set_line_type(self, line_type): 
        '''
        line_type: string
        '''
        self.line_type = line_type

    def display_all(self, x_values, y_values): 
        '''
        a method to actually show the display
        line: the line list plotted, need to be initialized to [] before first loop
        ax: int, index for the axis to plot
        x_values: list of x values
        y_values: list of y values
        '''
        if not(self.line): 
            # initialize figure if not
            plt.ion()
            self.line, = self.ax.plot(x_values,y_values, self.line_type)
            self.ax.set_xlabel(self.x_label)
            self.ax.set_ylabel(self.y_label)
            plt.show()
    
        # update data
        if self.y_lim: 
            self.ax.set_ylim(self.y_lim[0], self.y_lim[1])
        else: 
            self.ax.set_ylim(min(y_values)-5, max(y_values)+5)
        self.ax.set_xlim(min(x_values), max(x_values))
        self.line.set_ydata(y_values)
        self.line.set_xdata(x_values)


class DisplayRange(DisplayAll): 
    '''
    a class similar to DisplayAll, but only most recent part data are shown
    '''
    def __init__(self, ax, line_type='-o'): 
        super().__init__(ax, line_type)
        self.x_disp = [] # initialize display value pool
        self.y_disp = []
        self.n = 0 # initialize display value count
        
    
    def reset(self): 
        '''
        reset the pool
        '''
        self.x_disp = []
        self.y_disp = []
        self.n = 0 # reset display pool

    def display_range(self, x_values, y_values, range): 
        '''
        display over a range only
        x_values: list
        y_values: list
        range: int, number of points displayed
        '''
        if not(self.line): 
            # initialize figure if not
            plt.ion()
            self.line, = self.ax.plot(self.x_disp,self.y_disp, self.line_type)
            self.ax.set_xlabel(self.x_label)
            self.ax.set_ylabel(self.y_label)
            plt.show()

        
        # update display pool and update to line
        self.x_disp.append(x_values[self.n])
        self.y_disp.append(y_values[self.n])
        if len(self.x_disp) > range: 
            self.x_disp.pop(0)
            self.y_disp.pop(0)        
        if self.y_lim: 
            self.ax.set_ylim(self.y_lim[0], self.y_lim[1])
        else: 
            self.ax.set_ylim(min(y_values)-5, max(y_values)+5)
        self.ax.set_xlim(min(self.x_disp), max(self.x_disp))
        self.line.set_ydata(self.y_disp)
        self.line.set_xdata(self.x_disp)
        self.n = self.n+1
        


class DynamicMonitor(): 
    '''
    a class to display a intergrated panel for various information
    panel: tuple of int, (col, row) of subfigures
    size: tuple of int
    '''
    def __init__(self, panel, size): 
        self.panel = panel
        self.size = size
        self.fig, self.axis = set_figure_area.set_figure_area(panel[0], panel[1], size)
    
