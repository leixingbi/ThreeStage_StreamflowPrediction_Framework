"""
Dependencies:
https://emd.readthedocs.io/en/stable/install.html
"""
import sys

sys.path.append("../")

from PyEMD import EMD, CEEMDAN
from gensim.similarities import WmdSimilarity
from vmdpy import VMD
import numpy as np
import Auxiliary_code.Plot as plot
import numpy as np


def mini_distance(data_omega):
    c = np.sort(data_omega)
    status = 1
    for i in range(len(c) - 1):
        if np.abs((c[i] - c[i + 1]) / [c[i]]) <= 0.25:
            status = 0
            break
    return status


def vmd_decomposition(calibration_set, validation_set, method="hindcast_prediction"):
    for i in range(2, len(calibration_set) - 1):  # Find the optimal number of modes.
        # print("第%d次寻找最佳K值" % i)
        imfs, u_hat, omega = VMD(calibration_set, alpha=2000, tau=0., K=i, DC=0, init=1,
                                 tol=1e-7)  # K values according to EMD
        # print(omega)
        k_decision = [np.average(i) for i in omega.T]
        # print(k_decision)
        loop_decision = mini_distance(k_decision)
        # print(loop_decision)
        if loop_decision == 1:
            continue
        else:
            print("Meet stop conditions   ", i)
            break
    optimal_imf_num = i - 1
    imfs_train, u_hat, omega = VMD(calibration_set, alpha=2000, tau=0., K=i - 1, DC=0, init=1,
                                   tol=1e-7)  # K values according to EMD
    imfs_test, u_hat, omega = VMD(np.append(calibration_set, validation_set), alpha=2000, tau=0., K=i - 1, DC=0, init=1,
                                  tol=1e-7)  # K values according to EMD
    if method == "hindcast_prediction":
        return imfs_test[:, 0:len(calibration_set)], imfs_test, optimal_imf_num
    else:
        return imfs_train, imfs_test, optimal_imf_num



def emd_decomposition(calibration_set, validation_set, method="hindcast_prediction"):
    emd = EMD()
    imfs_all = emd(np.append(calibration_set, validation_set))
    if method == "hindcast_prediction":
        return imfs_all[:, 0:len(calibration_set)], imfs_all


def ceemdan_decomposition(calibration_set, validation_set, method="hindcast_prediction"):
    ceemdan = CEEMDAN()
    imfs_all = ceemdan(np.append(calibration_set, validation_set))
    if method == "hindcast_prediction":
        return imfs_all[:, 0:len(calibration_set)], imfs_all

