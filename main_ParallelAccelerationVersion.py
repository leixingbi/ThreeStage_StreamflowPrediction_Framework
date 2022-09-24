# -*- coding:utf-8 -*-

"""
functions:
    Three-stage Frame for Monthly Streamflow Forecasting:
    Stage 1：Non-stationary assessment; Stage 2：Decomposition-based modeling; Stage 3： Reconstruction

Dependencies
This framework requires:
    https://www.mathworks.com/products/new_products/release2020b.html  For matlab codes compilation Note: version=R2020b
    https://www.python.org/downloads/windows/                  For python codes compilation        Note: version=3.8.1
    https://github.com/zhaokg/Rbeast                           Rbeast project, For  Non-stationary assessment
    https://pypi.org/project/vmdpy/                            For VMD decomposition  For  Data stationarization
    https://pypi.org/project/EMD-signal/                       For EMD and CEEMDAN decomposition   Note: version=0.2.1.5  For  Data stationarization
    https://pypi.org/project/ewtpy/                            For EWT decomposition    For  Data stationarization
    https://pypi.org/project/scikit-learn/                     For SVR (Support vector regression machine) For modeling
    https://pypi.org/project/scikit-opt/                       For parameters optimization.
    https://docs.xlwings.org                                   For reading data from Excel file  (data management)
    https://openpyxl.readthedocs.io/                           For outputting the results to an Excel file
    multiprocessing                                            For computing acceleration  Note: python standard library


Detail Python version and Computer hardware:
    Python 3.8.1 (tags/v3.8.1:1b293b6, Dec 18 2019, 23:11:46) [MSC v.1916 64 bit (AMD64)] on win32
    CPU: Intel(R) Core(TM) i5-12400F   2.50 GHz
    GPU: NVIDIA GTX 1650 Super

Version 1.0  Multi-process version
Development time  : 2022-04-16
The last edit time: 2022-09-13  (Note: Adding a graphical user interface)

Notes: Supported by leixingbi@gxu.edu.com, leixingbi@foxmail.com
"""


import os
import sys
import numpy as np
from multiprocessing import Manager
from multiprocessing import Pool
import random
import time
from Auxiliary_code.Notice import send_notice

from Auxiliary_code.func1_Read_data import func1_read_data                  # read data from Excel file
from Nonstationary_assessment import Bayesian_statistics                    # assess the non-stationarity of data
from Auxiliary_code.func2_Decomposition_return import func2_decomposition   # stationary the origin  data
import Standard_model.SVR as SVR                                            # create a support victor machine model
from Auxiliary_code.func3_train_svm import func3_svr_train                  # train the support victor machine model
from Reconstruction_method.IRM import reconstruction as MER                 # reconstructed streamflow predictions
from Auxiliary_code.log import log_                                         # log the operation status
from Auxiliary_code.Output_to_Excel import to_excel                         # output the result
from Auxiliary_code.Result_report import result_report as report            # form a report


# For reproduction
np.random.seed(2)
random.seed(2)

if __name__ == '__main__':
    log_("begin")                 # Record historical operation logs

    # -------------------------------Custom parameters-----------------------------------------
    file_name = "DATA.xls"         # an Excel data file
    sheet_name = "Sheet1"          # data location in the Excel file
    column_index = "E"             # column "C" is CR basin,  "D" is FYR basin, "F" is NPR basin
    total_data = 660               # the period length of a given monthly stream-flow time series data
    train_ratio = 0.8              # The proportion of data used for model training
    max_lag = 10                   # max lag = max_lag + 2 , max_lag = 10 adopted here
    object_name = "rmse"           # the fitness function of PSO algorithm
    data_start_time = [1963, 1]    # Recording time of the first data
    # -----------------------------------------------------------------------------------------

    notes_information = [["study basin", column_index], ["train_ratio", train_ratio], ["max_lag", max_lag],
                         ["object_name", object_name]]
    to_excel(data=notes_information, method="information", file_name="multi_process")

    # ---------read data------
    data = func1_read_data(path=os.getcwd(), file_name=file_name, sheet_name=sheet_name,
                           column_index=column_index, total_column=total_data)
    data = np.array(data)

    # ------------------------------stage 1 ---Non-stationary assessment------------------------
    os.chdir('./Nonstationary_assessment/')
    stationary_prob = Bayesian_statistics.non_stationary_assess(origin_data=data, data_start_time=data_start_time)
    print("The probability that the monthly data is stationary:", stationary_prob)
    print("The probability that the monthly data is non-stationary:", 1 - stationary_prob)
    if stationary_prob > 0.5:
        print("The monthly data is stationary and we recommend that users model this data using a traditional "
              "statistical model, such as an autoregressive model.")
        sys.exit()  #

    print("\n ###################################################\n"
          "The monthly data is non-stationary and thus the Stage-2 \"stationarization-based modeling\" will be executed"
          "\n ###################################################\n")

    os.chdir('../')
    # --------------------------------------------------------------------------------------------

    # -------------------------------stage 2 stationarization-based modeling ---------------------
    model = ["svm", "vmd_svm", "emd_svm", "ceemdan_svm"]
    for model_i in model:
        prediction_options = model_i    # [svm, vmd_svm,emd_svm, ceemdan_svm]
        # ------------------------------stage 2-1 ---stationarization-----------------------------
        if prediction_options == "vmd_svm":
            imfs_train, imfs_test = func2_decomposition(data=data, train_ratio=train_ratio, method="VMD")
            imfs_all_vmd = np.append(imfs_train, imfs_test[:, int(total_data * train_ratio):], axis=1)
        elif prediction_options == "emd_svm":
            imfs_train, imfs_test = func2_decomposition(data=data, train_ratio=train_ratio, method="EMD")
            imfs_all_emd = np.append(imfs_train, imfs_test[:, int(total_data * train_ratio):], axis=1)
        elif prediction_options == "ceemdan_svm":
            imfs_train, imfs_test = func2_decomposition(data=data, train_ratio=train_ratio, method="CEEMDAN")
            imfs_all_ceemdan = np.append(imfs_train, imfs_test[:, int(total_data * train_ratio):], axis=1)

        # ------------------------------stage 2-2 ---Modeling--------------------------------------
        print("\nModeling processing is starting\n")
        object_func = func3_svr_train

        if prediction_options == "svm":
            base_data = data
        elif prediction_options == "vmd_svm":
            base_data = imfs_all_vmd
        elif prediction_options == "emd_svm":
            base_data = imfs_all_emd
        elif prediction_options == "ceemdan_svm":
            base_data = imfs_all_ceemdan

        if base_data.ndim == 1:
            # Asynchronous parallel computing is used to accelerate modeling
            pool = Pool(7)
            predicted_result = np.zeros(len(base_data))
            lags_result = Manager().list(np.zeros(max_lag))
            for lag_time in range(0, max_lag, 1):
                mulit_tast = pool.apply_async(object_func,
                                              args=(base_data, lag_time, train_ratio, object_name, lags_result))
            pool.close()
            pool.join()

            lags_result = np.array(lags_result)
            # print("The training optimal rmse sequence is: ", lags_result)
            return_value = np.array(lags_result)
            optimal_lag_object = min(lags_result)
            for i in range(len(lags_result)):
                if optimal_lag_object == lags_result[i]:
                    optimal_lag = i + 2
            np.random.seed(2)
            result_svr_imfs = SVR.svr_model(data, lag_time=optimal_lag,
                                            train_ratio=train_ratio, object_name=object_name)
            predicted_result[optimal_lag:] = result_svr_imfs
        if base_data.ndim == 2:
            imfs_num, value_num = base_data.shape
            predicted_result = np.zeros([imfs_num, value_num])
            lag_optimal = np.zeros(imfs_num)
            for optimal_lag_single_imf in range(imfs_num):
                pool = Pool(5)
                # print("-----------\n optimal lag search,imf No.", optimal_lag_single_imf + 1)
                single_imf_lag_object = np.zeros(max_lag)

                lags_result = Manager().list(np.zeros(max_lag))
                for lag_time in range(0, max_lag, 1):
                    mulit_tast = pool.apply_async(object_func,
                                                  args=(
                                                      base_data[optimal_lag_single_imf, :], lag_time, train_ratio,
                                                      object_name,
                                                      lags_result))
                pool.close()
                pool.join()

                single_imf_lag_object = np.array(lags_result)
                lag_optimal_objective = min(single_imf_lag_object)
                for lag_i in range(max_lag):
                    if lag_optimal_objective == single_imf_lag_object[lag_i]:
                        lag_optimal[optimal_lag_single_imf] = lag_i + 2
            for svr_imfs in range(imfs_num):
                data_imfs = base_data[svr_imfs, :]
                np.random.seed(2)
                result_svr_imfs = SVR.svr_model(data=data_imfs, lag_time=int(lag_optimal[svr_imfs]),
                                                train_ratio=train_ratio, object_name=object_name)
                predicted_result[svr_imfs, int(lag_optimal[svr_imfs]):] = result_svr_imfs

        # -----Results and Analysis ---------
        to_excel(data=data, method="raw_series", file_name="multi_process")

        if prediction_options == "svm":
            to_excel(data=predicted_result, method=prediction_options + "_Data", file_name="multi_process")
            print("SVM REPORT\n, rmse_test, nse_test, mae_test\n",
                  report(observed_value=data, predicted_value=predicted_result, train_ratio=train_ratio,
                         method=prediction_options))
        else:
            # --------------------------------stage 3 ---Reconstruction--------------------------
            # -------------------------stage 3.1 ---Reconstruction by traditional summation method (TSM)-----------
            # Output the prediction results of traditional decomposition-based methods to an Excel file
            to_excel(data=predicted_result, method=prediction_options + "_Data", file_name="multi_process")
            print(prediction_options + "_TSM", " REPORT\n rmse_test, nse_test, mae_test\n",
                  report(observed_value=data, predicted_value=predicted_result.sum(axis=0), train_ratio=train_ratio,
                         method=prediction_options + "-TSM_rpt"))

            # --------------------------stage 3.2 ---Reconstruction by minimum error reconstruction(MER)-----------
            reconstruc_value = MER(imfs_prediction=predicted_result, observed_streamflow=data,
                                              train_ratio=train_ratio)
            to_excel(data=reconstruc_value, method=prediction_options + "_MER_Data", file_name="multi_process")

            print(prediction_options + "_MER", " --REPORT---\n Notes: skipping train phase \n",
                  "rmse_test, nse_test, mae_test\n",
                  report(observed_value=data, predicted_value=reconstruc_value, train_ratio=train_ratio,
                         method=prediction_options + "_MER_rpt"))

    print("Program finish")
