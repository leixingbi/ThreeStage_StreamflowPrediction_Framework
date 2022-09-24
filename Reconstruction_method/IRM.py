# -*- coding:utf-8 -*-
"""
Reconstuction for reducing predictive errors
Time-frequency decomposition-based prediction methods (Stationarization-based methods)

https://pypi.org/project/scikit-opt/    For parameters optimization.

Version time: 2022-04-06  support by  leixingbi@foxmail.com
"""

import numpy as np
from sko.GA import GA
import sys
sys.path.append("../")
from Auxiliary_code.Optimization_algorithm import Reconstruction_GA


def reconstruction(imfs_prediction, observed_streamflow, train_ratio):
    # Step 01, Minimizing the error superposition problem by determining
    # the optimal contribution of the subsequence to the prediction result
    best_contribution = Reconstruction_GA.reconstruction_ga_return(Reconstruction_GA,
                                                                   imfs_prediction=imfs_prediction,
                                                                   observed_streamflow=observed_streamflow,
                                                                   train_ratio=train_ratio
                                                                   )
    contrib_based_imfs_sum = np.zeros(imfs_prediction.shape[1])
    for j in range(len(contrib_based_imfs_sum)):
        for i in range(imfs_prediction.shape[0]):
            contrib_based_imfs_sum[j] = contrib_based_imfs_sum[j] + imfs_prediction[i, j] * best_contribution[i]

    measured_values = observed_streamflow
    precicted_values = contrib_based_imfs_sum

    # Step 02： minimizing systematic errors by probability distribution mapping methods
    reconstruction_value = np.zeros(len(measured_values))

    for loop in range(int(train_ratio*len(measured_values)), len(measured_values), 1):  # train_data_length = 528
        station_value = measured_values[0:loop]  #
        predicted_for_reconstr = precicted_values[0:loop + 1]
        # ----------------QM---------------------------------
        max_station = np.max(station_value)
        min_station = np.min(station_value)
        max_predicted = np.max(predicted_for_reconstr)
        min_predicted = np.min(predicted_for_reconstr)

        sub_group_station = np.linspace(min_station, max_station, 100)
        sub_group_ecmwf = np.linspace(min_predicted, max_predicted, 100)

        station_value_sort = np.sort(station_value)
        ecmwf_value_sort = np.sort(predicted_for_reconstr)
        ECDF_observed = np.zeros(100)
        ECDF_predicted = np.zeros(100)
        total_column = len(station_value)
        for i in range(len(station_value)):
            for j in range(100):
                if station_value[i] <= sub_group_station[j]:
                    ECDF_observed[j] = ECDF_observed[j] + (1 / total_column)

        for i in range(len(predicted_for_reconstr)):
            for j in range(100):
                if predicted_for_reconstr[i] <= sub_group_ecmwf[j]:
                    ECDF_predicted[j] = ECDF_predicted[j] + (1 / total_column)

        # -----------correct_process--------------
        for j in range(100):
            # The first grouping value that is larger than the measured value.
            # 1. Find the position where the measured value has the same probability as the predicted value.
            if predicted_for_reconstr[loop] <= sub_group_ecmwf[j]:
                if j != 0:
                    # Linear interpolation method
                    position = (predicted_for_reconstr[loop] - sub_group_ecmwf[j - 1]) / (
                                sub_group_ecmwf[j] - sub_group_ecmwf[j - 1])
                    position_ecdf = ECDF_predicted[j - 1] + ((ECDF_predicted[j] - ECDF_predicted[j - 1]) * position)
                else:
                    position_ecdf = ECDF_predicted[0]
                for z in range(100):
                    if position_ecdf <= ECDF_observed[z]:
                        if z != 0:
                            position_in_observation = (position_ecdf - ECDF_observed[z - 1]) / (ECDF_observed[z] - ECDF_observed[z - 1])
                            reconstruction_value[loop] = sub_group_station[z - 1] + (
                                        (sub_group_station[z] - sub_group_station[z - 1]) * position_in_observation)
                            break
                        else:
                            reconstruction_value[loop] = sub_group_station[0]
                            break
                break
    return reconstruction_value






