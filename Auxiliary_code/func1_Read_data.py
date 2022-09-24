import sys
sys.path.append("../")
import xlwings as xw
import numpy as np


# -----------Function 1: Read data--------------
def func1_read_data(path=None, file_name=None, sheet_name=None, column_index=None, total_column=None):
    """
    :param path: Data file path
    :param file_name:
    :param sheet_name:  Sheet table where the data is stored
    :param column_index: Column where the data is stored
    :param total_column:  Total number of observed data.
    :return: Data (series) extraction from Excel file
    """
    wb = xw.Book(file_name)
    sheet = wb.sheets[sheet_name]
    value_range = column_index + "2:" + column_index + str(total_column + 1)
    list_value = sheet.range(value_range).value
    data_read = [i for i in np.array(list_value)]
    return data_read