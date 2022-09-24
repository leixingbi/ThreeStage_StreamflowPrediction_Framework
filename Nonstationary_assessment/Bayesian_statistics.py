import numpy as np
import scipy.io as scio
import sys
import matlab
import matlab.engine

"""
Note: This module requires matlab 2020.
https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html  

https://www.mathworks.com/help/matlab/release-notes.html   For matlab codes compilation        Note: version=R2020b
https://github.com/zhaokg/Rbeast                           Rbeast project, For  Non-stationary assessment

"""


def non_stationary_assess(origin_data=None, data_start_time=None):
    if origin_data is None:
        print("error: Input data is Null")
        sys.exit(0)
    data_mat_format = np.array(origin_data.reshape(len(origin_data), 1))
    nonstationary_assess_data = {'__header__': "b'MATLAB 5.0 MAT-file, Platform: PCWIN64, Created on: Wed Jun 15 09:20:59 2022'", '__version__': '1.0', '__globals__': [],
                                 'nonstationary_assess_data': np.array(data_mat_format)}
    scio.savemat('nonstationary_assess_data.mat', nonstationary_assess_data)  # data used in Rbeast

    data_start_time_mat = {'__header__': "b'MATLAB 5.0 MAT-file, Platform: PCWIN64, Created on: Wed Jun 15 09:20:59 2022'", '__version__': '1.0', '__globals__': [],
                                 'data_start_time': np.array(data_start_time)}
    scio.savemat('data_start_time.mat', data_start_time_mat)  # parameter value need in Rbeast

    # --------------------
    data_start_time = str(data_start_time)
    eng = matlab.engine.start_matlab(data_start_time)

    print("-------------------------------------------------------------------")
    print("The following display is provided by Rbeast project\n")

    eng.NonstationaryAssessmentRbeast()  # Supported by open-resources Rbeast project

    print("The above display is provided by Rbeast project")
    print("-------------------------------------------------------------------\n")
    print("The non-stationarity assessment has been completed\n")

    f = open("result_NonstationaryAssess.txt", "r")
    f.seek(0, 0)
    line = f.readline()
    stationary_prob = []
    while line:
        if line == "| Ascii plot of probability distribution for number of chgpts (ncp) |\n":
            line = f.readline()
            line = f.readline()
            stationary_prob.append(float(line[14:19]))
            line = f.readline()
        line = f.readline()
    f.close()
    print("#####\nDetail result of Stage 1 is located in result_NonstationaryAssess.txt file in Nonstationary folder\n"
          "#####")
    return min(stationary_prob)

