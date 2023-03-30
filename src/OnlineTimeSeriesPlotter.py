# External Packages Import
import matplotlib.pyplot as plt
import numpy as np


class OnlineTimeSeriesPlotter:
    """
    This class has a buffer on size line_size. It is updated on real time with every call to the render method after
    calling init_plot() once
    """

    def __init__(self, line_size, y_min, y_max, threshold=None, number_of_lines=1):
        """
        constructor for the online time series plotter
        :param line_size: the size of the plotted line
        :param y_min: minimum y value in the figure
        :param y_max: maximum y value in the figure
        :param threshold: the threshold is plotted as a constant horizontal line
        """
        self.buffers = [np.zeros(line_size) for i in range(number_of_lines)]
        # self.line = None
        self.lines = [None for i in range(number_of_lines)]
        self.ax = None
        self.fig = None
        self.y_min = y_min
        self.y_max = y_max
        self.threshold = threshold

    def init_plot(self):
        """
        this method creates the figure that will be updated at real time
        :return: None
        """
        number_of_lines = len(self.lines)
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        plt.ylim([self.y_min, self.y_max])
        plt.ion()
        self.ax.axhline(y=self.threshold, color='r', linestyle='-')
        for i in range(number_of_lines):
            self.lines[i], = self.ax.plot(self.buffers[i], '-',  label=f'Line {i}')  # Returns a tuple of line objects, thus the comma
            
        plt.show()

    def render(self, xs):
        """
        adds new sample x to buffer and updates the figure
        :param x:
        :return:
        """
        # self.buffer = np.concatenate([self.buffer[1:], [x]])  # update the buffer

        num_lines = len(self.lines)
        for i in range(num_lines):
            self.buffers[i] = np.concatenate([self.buffers[i][1:], [xs[i]]])
            self.lines[i].set_ydata(self.buffers[i])
        
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.001)
        
def test_online_time_series_plotter():
    line_size = 100
    y_min = -10
    y_max = 10
    threshold = 0

    plotter = OnlineTimeSeriesPlotter(line_size, y_min, y_max, threshold, 3)
    plotter.init_plot()

    # generate random data and render it on the plot
    for i in range(1000):
        x = np.random.uniform(-1, 1)
        y = np.random.uniform(-3, -2)
        z = np.random.uniform(4, 5)
        plotter.render([x, y, z])


if __name__ == '__main__':
    test_online_time_series_plotter()