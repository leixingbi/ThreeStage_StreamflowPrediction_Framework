# -*- coding:utf-8 -*-
"""
Function:
    Predicted results report

"""

import sys

sys.path.append("../")
from Auxiliary_code.Performance_indictor import rmse, nse, mae
from Auxiliary_code.Output_to_Excel import to_excel


def result_report(observed_value, predicted_value, train_ratio, method):
    observed_values_train = observed_value[:int(len(observed_value) * train_ratio)]
    observed_values_test = observed_value[int(len(observed_value) * train_ratio):]
    predicted_values_train = predicted_value[:int(len(observed_value) * train_ratio)]
    predicted_values_test = predicted_value[int(len(observed_value) * train_ratio):]
    rmse_train = rmse(observed_values_train, predicted_values_train)
    rmse_test = rmse(observed_values_test, predicted_values_test)
    nse_train = nse(observed_values_train, predicted_values_train)
    nse_test = nse(observed_values_test, predicted_values_test)
    mae_train = mae(observed_values_train, predicted_values_train)
    mae_test = mae(observed_values_test, predicted_values_test)
    to_excel_txt = [[method, " "], ["rmse_train", rmse_train], ["rmse_test", rmse_test],
                    ["nse_train", nse_train], ["nse_test", nse_test],
                    ["mae_train", mae_train],
                    ["mae_test", mae_test]
                    ]
    to_excel(data=to_excel_txt, method=method,  file_name="multi_process")

    return rmse_test, nse_test, mae_test
