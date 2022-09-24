# -*- coding:utf-8 -*-
import sys

sys.path.append("../")
from sklearn import svm
import numpy as np
import Auxiliary_code.Optimization_algorithm as OA  # For PSO parameters optimization
from Auxiliary_code.Norm_tool import Norm_equ
import random

np.random.seed(2)
random.seed(2)


def svr_model(data, lag_time, train_ratio, object_name):
    """
    :param object_name: Parameter optimization's target function name.
    :param data:
    :param lag_time:
    :param train_ratio:
    :return: Predictive result include Train set and Validation set
    """

    # --------Convert data forms for svr format [input variables,expected value]-------
    data_length = len(data)
    data_matrix = np.zeros((int(data_length - lag_time), int(lag_time + 1)))
    normdata, min_value, max_value = Norm_equ(data=data, train_ratio=train_ratio)  # Data normalization

    index = 0
    for i in range(int(data_length - lag_time)):  # Convert to matrix form
        for j in range(lag_time + 1):
            data_matrix[i, j] = normdata[index]
            index = index + 1
        index = index - lag_time

    train_data = data_matrix[:int(data_length * train_ratio) - lag_time, :]
    validation_data = data_matrix[int(data_length * train_ratio) - lag_time:, :]
    x_train = train_data[:, 0:-1]
    y_train = train_data[:, -1]
    x_all = data_matrix[:, 0:-1]

    # --------Model training process-------
    best_c_gamma_epsilon = OA.SVR_GA.ga_svr_return(OA.SVR_GA, x_train, y_train, object=object_name)
    C, gamma, epsilon = best_c_gamma_epsilon
    np.random.seed(2)
    model = svm.SVR(kernel="rbf", C=C, gamma=gamma, epsilon=epsilon)  # C=100, gamma=0.1, epsilon=0.1
    model.fit(x_train, y_train)
    # --------Model validation result-------
    result = model.predict(x_all)
    result_predict = [i * (max_value - min_value) + min_value for i in result]  # Revert to original data.

    result_predict = np.array(result_predict)
    return result_predict
