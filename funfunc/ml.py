# -*- coding: utf-8 -*-
# AUTHOR  : wjia
# TIME    : 2022/6/21 17:14
# FILE    : ml
# PROJECT : funfunc
# IDE     : PyCharm
import random


def pandas_max_print() -> None:
    import pandas as pd

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)


def train_test_split_arr(arr: list, ratio: float, shuffle=False):
    """
    @param arr:待拆分的列表
    @param ratio:希望得到的拆分后的列表数量的比例
    @param shuffle:是否随机打乱顺序
    @return:两个列表，第一个是长度比例为ratio的列表，第二个列表是raw列表拆出之后剩下的元素
    """
    if shuffle:
        random.shuffle(arr)

    length = len(arr)
    test_idx = random.sample(range(length), int(length * ratio))
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
