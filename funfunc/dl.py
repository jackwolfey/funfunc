# -*- coding: utf-8 -*-
# AUTHOR  : wjia
# TIME    : 2022/6/21 17:17
# FILE    : dl
# PROJECT : funfunc
# IDE     : PyCharm

def get_device_torch():
    import torch

    device = "cuda" if torch.cuda.is_available() else "cpu"
    return device
