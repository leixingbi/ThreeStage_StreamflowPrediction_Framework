# -*- coding:utf-8 -*-
"""
Function:
    Parameters of predictive model optimization

This module's dependencies:
    https://scikit-opt.github.io/scikit-opt/#/  Powerful Python module for Heuristic Algorithms
    https://pypi.org/project/scikit-learn/  For SVR (Support vector regression machine)

Version time: 2022-04-06  support by  leixingbi@foxmail.com
"""


from sko.PSO import PSO
from sklearn import svm
import random
import numpy as np
import sys

sys.path.append("../")
from Auxiliary_code.Performance_indictor import rmse, mape, nse

# --For reproduction --
np.random.seed(2)
random.seed(2)


class SVR_GA:
    """ Particle swarm algorithm to adjust SVM parameters   """
    """ Particle swarm algorithm to adjust SVM parameters """
    """ Note: The alternative of genetic algorithm to adjust the SVM parameters is also placed here"""
    def __init__(self, x_train, y_train, object2):
        global train_x
        global train_y
        global best_x
        global object_name
        object_name = object2
        train_x = np.array(x_train)
        train_y = np.array(y_train)
        n_x, n_y = train_x.shape

        # print("Parameters optimization (svm) under lag time=", n_y, "by using PSO algorithm",
        #       "           Note: Asynchronous parallel computing acceleration")

        # Note:--- cross-validation---
        # The lag time is considered as the main factor of the predictive model performance.
        # Therefore, cross-validation is simplified to "training(70%)- validation(30)", that is also known as
        # hand-out cross validation .
        # -----------------------

        # ---------PSO
        pso = PSO(func=self.func_ga, n_dim=3, pop=40, max_iter=150, lb=[0.01, 0.01, 0.01], ub=[100, 100, 100],
                  w=0.8, c1=0.5, c2=0.5)
        pso.run()
        best_x = pso.gbest_x
        best_y = pso.gbest_y

        # if object_name == "rmse":
        #     print("Optimization result", object2, "=", best_y[0], "Note: DATA is normalized")

        C, gamma, epsilon = best_x
        model = svm.SVR(kernel="rbf", C=C, gamma=gamma, epsilon=epsilon)
        model.fit(train_x, train_y)
        # print("train_phase:", object2, "=", rmse(train_y, np.array(model.predict(train_x))))

    def func_ga(self, x):
        C, gamma, epsilon = x
        model = svm.SVR(kernel="rbf", C=C, gamma=gamma, epsilon=epsilon)
        validation_ratio = 0.7
        model.fit(train_x[:int(len(train_y) * validation_ratio), :],
                  train_y[:int(len(train_y) * validation_ratio)])  # Prevent overfitting
        predicted_train_train = np.array(model.predict(train_x[:int(len(train_y) * validation_ratio), :]))
        predicted_train_test = np.array(model.predict(train_x[int(len(train_y) * validation_ratio):, :]))
        if object_name == "mape":
            mape_train = mape(train_y[:int(len(train_y) * validation_ratio)], predicted_train_train)
            mape_test = mape(train_y[int(len(train_y) * validation_ratio):], predicted_train_test)
            mean = mape_test
        if object_name == "rmse":
            rmse_train = rmse(train_y[:int(len(train_y) * validation_ratio)], predicted_train_train)
            rmse_test = rmse(train_y[int(len(train_y) * validation_ratio):], predicted_train_test)
            mean = rmse_test
        if object_name == "nse":
            nse_train = nse(train_y[:int(len(train_y) * validation_ratio)], predicted_train_train)
            nse_test = nse(train_y[int(len(train_y) * validation_ratio):], predicted_train_test)
            mean = 1 - nse_test
        return mean

    def ga_svr_return(self, x_train, y_train, object):
        SVR_GA(x_train=x_train, y_train=y_train, object2=object)
        return best_x


class Reconstruction_GA:
    """ Particle swarm algorithm to adjust the innovative reconstruction method (IRM) parameters """
    """ Note: The alternative of genetic algorithm to adjust the SVM parameters is also placed here"""
    def __init__(self, imfs_prediction, observed_streamflow, train_ratio):
        global imfs_prediction_ga
        global observed_streamflow_ga
        global train_ratio_ga
        global best_x
        train_ratio_ga = train_ratio
        imfs_prediction_ga = np.array(imfs_prediction)
        observed_streamflow_ga = np.array(observed_streamflow)
        imfs_mum, series_num = imfs_prediction_ga.shape

        lb = [0 for i in range(imfs_mum)]
        ub = [1 for i in range(imfs_mum)]

        # ---------PSO--------------
        pso = PSO(func=self.func_ga, n_dim=imfs_mum, pop=40, max_iter=150, lb=lb, ub=ub,
                  w=0.8, c1=0.5, c2=0.5)
        pso.run()
        best_x = pso.gbest_x
        best_y = pso.gbest_y

        # print('best_x(C,gamma,epsilon)):', best_x, '\n', 'best_y(rmse):', best_y)

    def func_ga(self, x):
        sum_imfs_train = np.zeros(imfs_prediction_ga.shape[1])
        for j in range(len(sum_imfs_train)):
            for i in range(imfs_prediction_ga.shape[0]):
                sum_imfs_train[j] = sum_imfs_train[j] + imfs_prediction_ga[i, j] * x[i]

        return rmse(observed_streamflow_ga[:int(len(observed_streamflow_ga) * train_ratio_ga)],
                    sum_imfs_train[:int(len(observed_streamflow_ga) * train_ratio_ga)])

    def reconstruction_ga_return(self, imfs_prediction, observed_streamflow, train_ratio):
        Reconstruction_GA(imfs_prediction=imfs_prediction, observed_streamflow=observed_streamflow,
                          train_ratio=train_ratio)
        return best_x
