# -*- coding:utf-8 -*-
"""
Function:
    Performance Indicators

"""
import numpy as np
from scipy import stats


# Notes:
#     "K" is used as a state or intermediate variable


def nse(except_values, simulate_values):
    K1 = 0
    K2 = 0
    mean_true = np.mean(except_values)
    for j in range(len(except_values)):
        K1 = K1 + ((except_values[j] - simulate_values[j]) * (except_values[j] - simulate_values[j]))
        K2 = K2 + ((except_values[j] - mean_true) * (except_values[j] - mean_true))
    NSE = 1 - (K1 / K2)
    return NSE


def r2(except_values, simulate_values):
    r = stats.pearsonr(simulate_values, except_values)
    r_2 = r[0] * r[0]
    return r_2


def rmse(except_values, simulate_values):
    K1 = 0
    for j in range(len(except_values)):
        K1 = K1 + ((except_values[j] - simulate_values[j]) * (except_values[j] - simulate_values[j]))
    RMSE = np.sqrt(K1 / len(except_values))
    return RMSE


def mape(except_values, simulate_values):
    K1 = 0
    for j in range(len(except_values)):
        if except_values[j] == 0:
            continue
        K1 = np.abs(((except_values[j] - simulate_values[j]) / (except_values[j]))) * 100 + K1
    MAPE = K1 / len(except_values)
    return MAPE


def mae(except_values, simulate_values):
    K1 = 0
    for j in range(len(except_values)):
        K1 = np.abs(except_values[j] - simulate_values[j]) + K1
    MAE = K1 / len(except_values)
    return MAE


def bias(except_values, simulate_values):
    total_bias = 0
    for j in range(len(except_values)):
        total_bias = total_bias + (except_values[j] - simulate_values[j])
        if j == len(except_values) - 1:
            bias = total_bias / len(except_values)


def indictor_precipitation(except_values, simulate_values):
    H = 0  # Precipitation events have been captured by both ground and satellite.
    M = 0  # precipitation events have been captured by the ground only.
    F = 0  # Satellite incorrectly captures rainfall events (no actual precipitation).
    for j in range(len(except_values)):
        if except_values[j] > 0 and simulate_values[j] > 0:
            H = H + 1
        if except_values[j] > 0 and simulate_values[j] == 0:
            M = M + 1
        if except_values[j] == 0 and simulate_values[j] > 0:
            F = F + 1
    POD = H / (H + M)
    FAR = F / (H + F)
    CSI = H / (H + M + F)
    return POD, FAR, CSI


def standard_deviation(data):
    data = np.array(data)
    return np.std(data)
