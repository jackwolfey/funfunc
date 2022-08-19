# -*- coding: utf-8 -*-
# AUTHOR  : wjia
# TIME    : 2022/6/21 17:14
# FILE    : ml
# PROJECT : funfunc
# IDE     : PyCharm
import random
from typing import Tuple, List


def pandas_max_print() -> None:
    import pandas as pd

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)


def train_test_split_arr(arr: list, ratio: float, shuffle=False) -> Tuple[List, List]:
    """
    @param arr: target list ready to split
    @param ratio: the train set ratio
    @param shuffle: shuffle arr
    @return: Tuple(train_set, test_set)
    """
    if shuffle:
        random.shuffle(arr)

    length = len(arr)
    test_idx = random.sample(range(length), length - (int(length * ratio)))
    train = []
    test = []

    index = [False for _ in range(length)]
    for i in test_idx:
        index[i] = True

    for i, element in enumerate(index):
        if element:
            test.append(arr[i])
        else:
            train.append(arr[i])
    return train, test
