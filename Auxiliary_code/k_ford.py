import numpy as np

"""
function:
    5-ford cross-validation data Segmentation
"""


def k_for(data, k):
    data = np.array(data)
    index_ratio = []
    equ_variant_value = 1 / k
    index_process = 0
    for i in range(k):
        index_process = index_process + equ_variant_value
        index_ratio.append(index_process)

    if data.ndim == 1:
        print("one dimision")
        for i in range(k):
            index_ratio[i] = int(len(data) * index_ratio[i])
        train = []
        validation = []
        for i in range(k):
            if i == 0:
                append_data = data[index_ratio[i]:]
                append_data = append_data.tolist()
                train.append(append_data)
                validation.append(data[0:index_ratio[i]])
            else:
                train_part1 = data[0:index_ratio[i - 1]]
                train_part2 = data[index_ratio[i]:]
                append_data = np.append(train_part1, train_part2)
                append_data = append_data.tolist()
                train.append(append_data)
                validation.append(data[index_ratio[i - 1]:index_ratio[i]])

    if data.ndim == 2:
        print("two dimision")
        cow_num, column_num = data.shape
        print(cow_num, column_num)
        for i in range(k):
            index_ratio[i] = int(cow_num * index_ratio[i])
        train = []
        validation = []
        for i in range(k):
            if i == 0:
                train.append(data[index_ratio[i]:, :])
                validation.append(data[0:index_ratio[i], :])
            else:
                train_part1 = data[0:index_ratio[i - 1], :]
                train_part2 = data[index_ratio[i]:, :]
                train.append(np.append(train_part1, train_part2, axis=0))
                validation.append(data[index_ratio[i - 1]:index_ratio[i]])
    # train = np.array(train)
    # validation = np.array(validation)
    return train, validation

