
Code and data repository for "A Robust Three-stage Framework for Monthly Streamflow Forecasting: Nonstationary assessment, Stationarization-based modeling, and Reconstruction"

Title:
Code and data for " A Robust Three-stage Framework for Monthly Streamflow Forecasting: Nonstationary assessment, Stationarization-based modeling, and Reconstruction "

Author:
Xingbi Lei (leixingbi@st.gxu.edu.cn, leixingbi@foxmail.com)

Institutions:
College of Architecture and Civil Engineering, Guangxi University, Nanning 530000, China

Categories:
hydro; surface water

Description:
This data repository contains code and data for the research article “A Robust Three-stage Framework for Monthly Streamflow Forecasting: Nonstationary assessment, Stationarization-based modeling, and Reconstruction”, which is currently under review for the journal Science of The Total Environment.

The data used in this study is the monthly streamflow data sets (1963/01-2017/12) of the Bashou, Fyras and Wyoming-Nebraska station in the Chengbi River basin (China), Fyran River basin (Sweden), and North Platte River basin (US), respectively. Those data are organized in “DATA.xls” file. It should be noted that due to policy limitations, the streamflow data collected from Bashou station are not published here. 

The fundamental code for stage 1 “Nonstationary assessment"，stage 2 “Stationarization-based modeling”, and stage 3 “Reconstruction” is organized in the “Nonstationary_assessment” directory, “Stationary_methods” directory combined with  “Standard_model” directory, and “Reconstruction_method” directory, respectively. 

To reproduce the results of this paper, follow the instructions given in readme.md. Note that the same results demonstrated in this paper cannot be reproduced but similar results should be reproduced.

Open-source software:

In this work, we employ multiple open-source projects and python language platform for framework implementation. Specifically, the “Rbeast” project to create Bayesian statistics for non-stationarity assessment, The PyEMD and Vmdpy projects to create decomposition algorithm (including EMD and CEEMDAN and VMD) for data stationarization; the Scikit-Learn project to create SVM model for modeling, and the Particle Swarm Optimization algorithm in the Scikit-opt project to tune the parameters of the SVM. The developed innovative reconstruction method is coded and compiled in python language. In addition, we use the Numpy (van der Walt et al., 2011) and Xlwings projects for data management, and the Multiprocessing module within python standard libraries to accelerate the computations.
All models are developed and tested based on the following Python version and Computer hardware:
Python 3.8.1 (tags/v3.8.1:1b293b6, Dec 18 2019, 23:11:46) [MSC v.1916 64 bit (AMD64)] on win32
CPU: Intel(R) Core(TM) i5-12400F   2.50 GHz
GPU: NVIDIA GTX 1650 Super

How to validate the research results
1. Clone this repository from GitHub. Run the following code in CMD or git-bash;

git clone https://github.com/leixingbi/ThreeStage_StreamflowPrediction_Framework

2. Open this repository with Pycharm software (or other IDEs);

3. Install the dependencies mentioned in Open-source software (or install all third-party libraries organized in the file “requirements.txt”)

3. Run the file “main_ParallelAccelerationVersion.py” in Pycharm IDE for the auto operation of the proposed framework methodology and its realizations;

Note that we provide a more detailed code(s) explanation within each file. The operation results are organized in the file “result_multi_process.xlsx”, “Result” directory.

Reference

Stéfan, v. d. W., Colbert, S. C., and Varoquaux, G.: The NumPy Array: A Structure for Efficient Numerical Computation: A Structure for Efficient Numerical Computation,Comput.Sci.Eng.,13,22–30, https://doi.org/10.1109/MCSE.2011.37, 2011   [NUMPY]
Abadi, M., Agarwal, A., Barham, P., Brevdo, E., Chen, Z., Citro, C., Corrado, G. S., Davis, A., Dean, J., Devin, M., Ghemawat, S., Goodfellow, I., Harp, A., Irving, G., Isard, M., Jia, Y., Jozefowicz, R., Kaiser, L., Kudlur, M., Levenberg, J., Mane, D., Monga, R., Moore, S., Murray, D., Olah, C., Schuster, M., Shlens, J., Steiner, B., Sutskever, I., Talwar, K., Tucker, P., Vanhoucke, V., Vasudevan, V., Viegas, F., Vinyals, O., Warden, P., Wattenberg, M., Wicke, M., Yu, Y., and Zheng, X.: TensorFlow: Large-Scale Machine Learning on Heterogeneous Distributed Systems, 2016.
McKinney, W., 2010. Data Structures for Statistical Computing in Python, pp. 51–56.
Stéfan, v.d.W., Colbert, S.C., Varoquaux, G., 2011. The NumPy Array: A Structure for Efficient Numerical Computation. A Structure for Efficient Numerical Computation. Comput. Sci. Eng. 13 (2), 22–30.
Dragomiretskiy, K., Zosso, D., 2014. Variational Mode Decomposition. IEEE Trans. Signal Process. 62 (3), 531–544.
Wu, Z., Huang, N.E., 2009. Ensemble Empirical Mode Decomposition: a Noise-Assisted Data Analysis Method. Adv. Adapt. Data Anal. 01 (01), 1–41.
Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., Duchesnay, É., 2011. Scikit-learn. Machine Learning in Python. Journal of Machine Learning Research 12, 2825–2830.
Tim, H., MechCoder, Gilles, L., Iaroslav, S., fcharras, Zé Vinícius, cmmalone, Christopher, S., nel215, Nuno, C., Todd, Y., Stefano, C., Thomas, F., rene-rex, Kejia, (K.) S., Justus, S., carlosdanielcsantos, Hvass-Labs, Mikhail, P., SoManyUsernamesTaken, Fred, C., Loïc, E., Lilian, B., Mehdi, C., Karlson, P., Fabian, L., Christophe, C., Anna, G., Andreas, M., and Alexander, F.: Scikit-Optimize/Scikit-Optimize: V0.5.2, Zenodo, 2018.
Hunter, J.D., 2007. Matplotlib. A 2D Graphics Environment. Computing in Science & Engineering 9, 90–95.
Jordan D'Arcy: Introducing SSA for Time Series Decomposition, Kaggle, 4/29/2018, https://www.kaggle.com/jdarcy/introducing-ssa-for-time-series-decomposition, last access: 28 April 2020.966Z, 2018.
