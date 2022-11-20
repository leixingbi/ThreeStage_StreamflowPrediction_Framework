Title:
Code and data repository for "A Robust Three-stage Framework for Monthly Streamflow Forecasting: Nonstationary assessment, Stationarization-based modeling, and Reconstruction"

Author:
Xingbi Lei (leixingbi@st.gxu.edu.cn, leixingbi@foxmail.com)

Institutions:
College of Architecture and Civil Engineering, Guangxi University, Nanning 530000, China

Categories:
hydro; surface water

Description:

This data repository contains code and data for the research article “A Robust Three-stage Framework for Monthly Streamflow Forecasting: Nonstationary assessment, Stationarization-based modeling, and Reconstruction”, which is currently under review for the journal "Journal of Cleaner Production".

The data used in this study is the monthly streamflow data sets (1963/01-2017/12) of the Bashou, Fyras and Wyoming-Nebraska stations in the Chengbi River basin (China), Fyran River basin (Sweden), and North Platte River basin (US), respectively. Those data are organized in the “DATA.xls” file. It should be noted that due to policy limitations, the streamflow data collected from Bashou station are not published here. 

The fundamental code for stage 1 “Nonstationary assessment"， stage 2 “Stationarization-based modeling”, and stage 3 “Reconstruction” is organized in the “Nonstationary_assessment” directory, “Stationary_methods” directory combined with the “Standard_model” directory, and “Reconstruction_method” directory, respectively. 

To reproduce the results of this paper, follow the instructions given in readme.md. Note that the same results demonstrated in this paper cannot be reproduced but similar results should be reproduced.

Open-source software:
 
In this work, we employ multiple open-source projects and python language platform for the software implementation of the proposed framework. Specifically, the “Beast” project to create Bayesian statistics for non-stationarity assessment, The EMD-signal and Vmdpy projects to create decomposition algorithms (including EMD and CEEMDAN and VMD) for data stationarization; the Scikit-Learn project to create SVM model for modeling, and the Particle Swarm Optimization algorithm in the Scikit-opt project to tune the parameters of the SVM and of the developed innovative reconstruction method. The developed innovative reconstruction method is coded and compiled in python language. In addition, we use the Numpy (van der Walt et al., 2011) and Xlwings projects for data management, and the Multiprocessing module within python standard libraries to accelerate the computations.
All models are developed and tested based on the following Python version and Computer hardware:
Python 3.8.1 (tags/v3.8.1:1b293b6, Dec 18 2019, 23:11:46) [MSC v.1916 64 bit (AMD64)] on win32
CPU: Intel(R) Core(TM) i5-12400F   2.50 GHz
GPU: NVIDIA GTX 1650 Super

How to validate the research results
1. Clone this repository from GitHub. Run the following code in CMD or git-bash;

git clone https://github.com/leixingbi/ThreeStage_StreamflowPrediction_Framework

2. Open this repository with Pycharm software (or other IDEs);

3. Install the dependencies mentioned in Open-source software (or install the third-party libraries organized in the file “requirements.txt”)

3. Run the file “main_ParallelAccelerationVersion.py” in Pycharm IDE for the auto operation of the proposed framework methodology and its realizations;

Note that we provide a more detailed code(s) explanation within each file. In this software implementation, We name the innovative reconstruction method as minimum error reconstruction (MER). The operation results are organized in the file “result_multi_process.xlsx”, “Result” directory.

Reference

Zhao, K. et al., 2019. Detecting change-point, trend, and seasonality in satellite time series data to track abrupt changes and nonlinear dynamics: A Bayesian ensemble algorithm. Remote Sensing of Environment, 232: 111181.https://doi.org/10.1016/j.rse.2019.04.034

Stéfan, v. d. W., Colbert, S. C., and Varoquaux, G.: The NumPy Array: A Structure for Efficient Numerical Computation: A Structure for Efficient Numerical Computation,Comput.Sci.Eng.,13,22–30, https://doi.org/10.1109/MCSE.2011.37, 2011

Ofir Pele and Michael Werman. Fast and robust earth mover’s distances. Proc. 2009 IEEE 12th Int. Conf. on Computer Vision, Kyoto, Japan, 2009, pp. 460-467.

Vinícius R. Carvalho, Márcio F.D. Moraes, Antônio P. Braga, Eduardo M.A.M. Mendes, Evaluating five different adaptive decomposition methods for EEG signal seizure detection and classification, Biomedical Signal Processing and Control, Volume 62, 2020, 102073, ISSN 1746-8094, https://doi.org/10.1016/j.bspc.2020.102073.

https://github.com/zhaokg/Rbeast  (last access: 17 September 2022).

https://scikit-learn.org/stable/about.html#citing-scikit-learn (last access: 17 September 2022).

https://pypi.org/project/EMD-signal/ (last access: 17 September 2022).

https://pypi.org/project/scikit-opt/ (last access: 17 September 2022).

https://pypi.org/project/scikit-learn/ (last access: 17 September 2022).

https://pypi.org/project/xlwings/ (last access: 17 September 2022).

https://pypi.org/project/numpy/(last access: 17 September 2022).
