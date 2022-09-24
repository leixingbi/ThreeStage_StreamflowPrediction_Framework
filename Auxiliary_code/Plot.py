# -*- coding:utf-8 -*-
"""
Function:
    Results preview

"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append("../")


def plot_for_view(data, label=None):
    y = np.array(data)
    if y.ndim == 1:  # One-dimensional time series
        b = len(y)
        x = np.arange(1, b + 1, 1)
        fig, ax = plt.subplots()
        ax.plot(x, y)
        plt.show()
    if y.ndim == 2:  # Two-dimensional time series
        a, b = y.shape
        x = np.arange(1, b + 1, 1)
        fig, ax = plt.subplots()
        for j in range(a):
            ax.plot(x, y[j, :])
        plt.show()
