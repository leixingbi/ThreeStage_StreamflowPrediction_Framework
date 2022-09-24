"""
Function:
    Time series normalization
"""

import numpy as np
import sys
sys.path.append("../")


def Norm_equ(data, train_ratio):
    data_train, data_test = data[:int(len(data) * train_ratio)], data[int(len(data) * train_ratio):]
    min_value_all = np.min(data)
    max_value_all = np.max(data)
    Norm = [((i-min_value_all)/(max_value_all-min_value_all)) for i in data]
    Norm_test = Norm[int(len(data) * train_ratio):]

    min_value_train = np.min(data_train)
    max_value_train = np.max(data_train)
    Norm_train = [(i-min_value_train)/(max_value_train-min_value_train) for i in data]

    norm_for_model = np.append(Norm_train[:int(len(data) * train_ratio)], Norm_test)

    return norm_for_model, min_value_train, max_value_train
