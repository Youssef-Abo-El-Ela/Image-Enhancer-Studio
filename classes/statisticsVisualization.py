import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class HistogramCanvas(FigureCanvas):
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(5, 4) , facecolor='#1E293B')
        super().__init__(self.fig)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()
        self.ax.axes.set_axis_off()

    def plot_histogram(self, image):
        histogram = np.zeros(256)
        for pixel in image.ravel():
            histogram[pixel] += 1

        self.ax.clear()
        self.ax.set_facecolor('#1E293B') 
        self.fig.patch.set_facecolor('#1E293B')
        self.ax.bar(range(256), histogram, color='white', width=5)
        self.ax.tick_params(axis='both', colors="white") 
        for spine in self.ax.spines.values():
            spine.set_edgecolor('white')  
            spine.set_linewidth(2) 
        self.fig.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.15)
        self.draw()

class CDFCanvas(FigureCanvas):
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(5, 4) , facecolor='#1E293B')
        super().__init__(self.fig)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()
        self.ax.axes.set_axis_off()

    def plot_cdf(self, image):
        histogram = np.zeros(256)
        for pixel in image.ravel():
            histogram[pixel] += 1

        pdf = histogram / histogram.sum()

        self.ax.clear()
        self.ax.set_facecolor('#1E293B')  
        self.fig.patch.set_facecolor('#1E293B')
        self.ax.plot(pdf, color='white')
        self.ax.tick_params(axis='both', colors="white") 
        for spine in self.ax.spines.values():
            spine.set_edgecolor('white')  
            spine.set_linewidth(2) 
        self.fig.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.15)
        self.draw()
