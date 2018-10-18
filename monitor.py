#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import tkinter as tk
import matplotlib.animation as animation

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import font

import util
from arduinoiface import Reader

PROPS = util.get_config()


class CustomWidget:
    """
    Abstract class for all widgets. 

    The create_widghets method is to be overwritten so that the
    widget may be properly intialized.
    """

    def create_widgets(self):
        raise NotImplementedError


class InfoFrame(tk.Frame, CustomWidget):
    bgcolor = util.rgb(41, 43, 44)
    txcolor = util.rgb(255, 255, 255)

    def __init__(self, master):
        super(InfoFrame, self).__init__(master, background=InfoFrame.bgcolor)
        self.pack(side=tk.LEFT, fill=tk.BOTH)

        self.create_widgets()

    def create_widgets(self):

        lblfont = font.Font(family="Verdana")

        tk.Label(self, font=lblfont, background=InfoFrame.bgcolor, foreground=InfoFrame.txcolor,
                 text="Instituto Politecnico Nacional\nEscuela Superior de Computo\n").grid(row=0, columnspan=2)
        tk.Label(self, font=lblfont, background=InfoFrame.bgcolor, foreground=InfoFrame.txcolor,
                 text="Instrumentacion").grid(row=1, column=0)
        tk.Label(self, font=lblfont, background=InfoFrame.bgcolor, foreground=InfoFrame.txcolor,
                 text=PROPS["grupo"]).grid(row=1, column=1)

        names = PROPS["integrantes"].split(";")
        lblteam = tk.Label(self, font=lblfont, background=InfoFrame.bgcolor, foreground=InfoFrame.txcolor,
                           justify="left", text='\n'.join(names))
        lblteam.grid(row=3, columnspan=2)

        self.measurement = tk.DoubleVar(self, value=0)
        tk.Entry(self, text="Valor de prueba", justify="center", state="readonly",
                 textvariable=self.measurement, width=10).grid(row=5, column=0)
        tk.Label(self, font=lblfont, background=InfoFrame.bgcolor, foreground=InfoFrame.txcolor,
                 text="% de humedad").grid(row=5, column=1)

        self.grid_rowconfigure(2, minsize=100)
        self.grid_rowconfigure(4, minsize=50)


class MonitorCanvas(Figure, CustomWidget):
    def __init__(self, master):
        super(MonitorCanvas, self).__init__(figsize=(5, 4), dpi=100)
        self.master = master
        self.create_widgets()

        # Serial reader
        r = Reader(PROPS["port"], i.measurement)
        r.start()

    def create_widgets(self):
        ax = self.subplots()

        self.x = np.arange(0, 5, 0.01)
        self.y = [i for i in range(len(self.x))]
        self.line, = ax.plot(self.x, self.y)

        ax.set_ylabel("Porcentaje de humedad")
        ax.set_ybound(-1, 1)
        self.set_tight_layout(True)

        canvas = FigureCanvasTkAgg(self, master=self.master)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        ani = animation.FuncAnimation(
            self, self.animate, init_func=self.init,
            interval=2, blit=True, save_count=50)

        canvas.draw()

    def init(self):
        self.line.set_ydata([np.nan] * len(self.x))
        return self.line,

    def animate(self, i):
        self.line.set_ydata(np.sin(self.x + i / 100))
        return self.line,


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Sensor de humedad")

    i = InfoFrame(root)
    m = MonitorCanvas(root)

    root.mainloop()
