# -*- coding:utf-8 -*-
"""
functions:
    Three-stage Frame for Nonstationary Monthly Streamflow Forecasting:
    Decomposition, prediction, and Reconstruction

Notes: This program is based on the python platform

Dependencies
This framework requires:
    https://pypi.org/project/vmdpy/         For VMD decomposition
    https://pypi.org/project/ewtpy/         For EWT decomposition
    https://pypi.org/project/scikit-learn/  For SVR (Support vector regression machine)
    https://pypi.org/project/scikit-opt/    For parameters optimization.
    https://docs.xlwings.org                For reading data from Excel file
    https://openpyxl.readthedocs.io/        For outputting the results to an Excel file

Python version and Computer hardware:
    Python 3.8.5 (tags/v3.8.5:580fbb0, Jul 20 2020, 15:57:54) [MSC v.1924 64 bit (AMD64)] on win32
    Intel(R) Core(TM) i5-7400 CPU @ 3.00GHz   3.00 GHz

Version 1.0
Development time: 2022-04-06
Support by leixingbi@foxmail.com
"""

import xlwings as xw
import numpy as np
import Auxiliary_code.Plot as plot
import Standard_model.SVR as SVR
import Stationary_methods.Decomposition as sd
from Auxiliary_code.Performance_indictor import rmse, nse, mape
import os
from multiprocessing import Process as mp
import time
from Auxiliary_code.log import log_
import random
from Auxiliary_code.Output_to_Excel import to_excel
from Auxiliary_code.Result_report import result_report as report
from multiprocessing import Pool


# For reproduction
np.random.seed(2)
random.seed(2)


def func3_svr_train(data, lag_time, train_ratio, object_name, lags_result):
    np.random.seed(2)
    print("Parameters optimization (SVM) by using PSO algorithm",
          "           Note: Asynchronous parallel computing acceleration")
    # print(data, lag_time, train_ratio, object_name,return_value)
    # print("-----------\nInput lag time", lag_time+2, "Note: Parameter seeking is started")
    # start = time.perf_counter()

    lag_time = lag_time+2
    train_ratio = train_ratio
    data = np.array(data)
    result_svr = SVR.svr_model(data, lag_time=lag_time, train_ratio=train_ratio, object_name=object_name)

    data_train, data_test = data[lag_time:int(len(data) * train_ratio)], data[int(len(data) * train_ratio):]
    result_svr_train = result_svr[:int(len(data) * train_ratio) - lag_time]
    result_svr_test = result_svr[int(len(data) * train_ratio) - lag_time:]

    # ----------- Performance metrics in calibration set--------------------------------
    svr_rmse, svr_nse, svr_mape = rmse(data_train, result_svr_train), nse(data_train, result_svr_train), \
                                  mape(data_train, result_svr_train)

    # ----------- Performance metrics in Validation set--------------------------------
    svr_rmse_test, svr_nse_test, svr_mape_test = rmse(data_test, result_svr_test), \
                                                 nse(data_test, result_svr_test), \
                                                 mape(data_test, result_svr_test)

    # end = time.perf_counter()
    # print("The time consumed for modeling(unit is second):", str(end - start))

    log_("Calibration set: \n RMSE、NSE、MAPE:" + str(svr_rmse) + " " + str(svr_nse) + " " + str(svr_mape))
    log_("Validation  set: \n RMSE、NSE、MAPE:"
         + str(svr_rmse_test) + " " + str(svr_nse_test) + " " + str(svr_mape_test))

    if object_name == "rmse":
        return_object_value = svr_rmse
    elif object_name == "mape":
        return_object_value = svr_mape
    elif object_name == "nse":
        return_object_value = 1 - svr_nse
    else:
        print("objective %s is not be supported now " % str(object_name))
    lags_result[lag_time-2] = return_object_value
    # print("The value of nse for the prediction model with la", lag_time, "is", return_object_value)
    return lags_result