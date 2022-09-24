import sys
sys.path.append("../")
import Stationary_methods.Decomposition as sd
from Auxiliary_code.Output_to_Excel import to_excel


def func2_decomposition(data, train_ratio, method="VMD"):
    """
    :param data:
    :param train_ratio:
    :param method: Modal decomposition algorithm ( VMD and EWT support )
    :return: imfs_train, imfs_test, results of data decomposition of the training set and entirely series, respectively
    """
    calibration_set = data[:int(len(data) * train_ratio)]
    validation_set = data[int(len(data) * train_ratio):]

    if method == "VMD":
        imfs_train, imfs_test, optimal_imf_num = sd.vmd_decomposition(calibration_set=calibration_set,
                                                                      validation_set=validation_set)
        to_excel(data=imfs_train, method=method + "_imfs_train", file_name="multi_process")
        to_excel(data=imfs_test, method=method + "_imfs_test", file_name="multi_process")
    if method == "EWT":
        imfs_train, imfs_test = sd.ewt_decomposition(calibration_set=calibration_set,
                                                     validation_set=validation_set)
        to_excel(data=imfs_train, method=method + "_imfs_train", file_name="multi_process")
        to_excel(data=imfs_test, method=method + "_imfs_test", file_name="multi_process")
    if method == "EMD":
        imfs_train, imfs_test = sd.emd_decomposition(calibration_set=calibration_set,
                                                     validation_set=validation_set)
        to_excel(data=imfs_train, method=method + "_imfs_train", file_name="multi_process")
        to_excel(data=imfs_test, method=method + "_imfs_test", file_name="multi_process")

    if method == "EEMD":
        imfs_train, imfs_test = sd.eemd_decomposition(calibration_set=calibration_set,
                                                     validation_set=validation_set)
        to_excel(data=imfs_train, method=method + "_imfs_train", file_name="multi_process")
        to_excel(data=imfs_test, method=method + "_imfs_test", file_name="multi_process")

    if method == "CEEMDAN":
        imfs_train, imfs_test = sd.ceemdan_decomposition(calibration_set=calibration_set,
                                                     validation_set=validation_set)
        to_excel(data=imfs_train, method=method + "_imfs_train", file_name="multi_process")
        to_excel(data=imfs_test, method=method + "_imfs_test", file_name="multi_process")

    print("-----------\nStationarization (Decomposition) is complete")

    return imfs_train, imfs_test