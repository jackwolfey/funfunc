# -*- coding: utf-8 -*-
# AUTHOR  : wjia
# TIME    : 2022/6/21 17:08
# FILE    : tool
# PROJECT : funfunc
# IDE     : PyCharm
import datetime
import functools
import json
import logging
import os
import time
import warnings


def get_current_str_time() -> str:
    """get local time"""
    now_time = datetime.datetime.now()
    str_time = now_time.strftime('%Y年%m月%d日星期%w %H时%M分%S秒')
    return str_time


def download_file(url, save_path):
    """download a file by its url"""
    import requests

    r = requests.get(url, stream=True)
    with open(os.path.join(save_path), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)


def time_it(method):
    """use this decorator to print a function time cost"""

    @functools.wraps(method)
    def waapper(*args, **kwargs):
        start = time.time()
        result = method(*args, **kwargs)
        end = time.time()
        print('{} USED TIME:{}'.format(method.__name__, end - start))

        return result

    return waapper


def quick_sort(arr: list) -> list:
    """classic sort algorithm"""
    if len(arr) < 2:
        return arr
    temp = arr[0]
    small = [i for i in arr[1:] if i <= temp]
    big = [i for i in arr[1:] if i > temp]
    return quick_sort(small) + [temp] + quick_sort(big)


def get_basic_logger():
    """fast way to create a logging.Logger object"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger(__name__)
    return logger


def chunks(arr: list, n: int) -> list:
    """split list to n part"""
    return [arr[i:i + n] for i in range(0, len(arr), n)]


def get_host_ip():
    """check local ip"""
    import socket

    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def time_to_timestamp(date):
    """2000-10-20 12:10:30 format time to timestamp"""
    return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timestamp()


def second_to_strtime(second: int):
    """second to min:sec"""
    return time.strftime("%M:%S", time.gmtime(second))


def set_deprecated(warn_msg=None):
    """set a function into deprecated state"""

    def outer(deprecated_func):
        def inner(*args, **kwargs):
            if warn_msg and isinstance(warn_msg, str):
                warnings.warn(warn_msg, DeprecationWarning, 2)
            else:
                warnings.warn(f"This function {deprecated_func.__name__}() is deprecated!", DeprecationWarning, 2)
            core = deprecated_func(*args, **kwargs)
            return core

        return inner

    return outer


def indented_json_string(json_string):
    return json.dumps(json_string, indent=2, ensure_ascii=False)


class MagicDict(dict):
    """
    let you access python dict object by using attr
    Example:
        from funfunc import MagicDict

        simple_dict = {'name': 'Jack', 'age': 19, 'info': {'address': 'Beijing', 'phone': '123'}}
        magic_dict = MagicDict(simple_dict)
        print(magic_dict.name)
        # Jack
        print(magic_dict.info.address)
        # Beijing
    """

    # inherit from built-in class dict to automatically implement all dict original method
    def __init__(self, d=None, **kwargs):  # noqa
        if d is None:
            # empty init
            d = {}
        if kwargs:
            # support for update feature
            d.update(**kwargs)
        for k, v in d.items():
            # set class attribute
            setattr(self, k, v)

        for k in self.__class__.__dict__.keys():
            # ignore any magic method and useful method
            if not (k.startswith('__') and k.endswith('__')) and k not in ('update', 'pop'):
                setattr(self, k, getattr(self, k))

    def __setattr__(self, name, value):
        if isinstance(value, (list, tuple)):
            value = [self.__class__(x)
                     if isinstance(x, dict) else x for x in value]
        elif isinstance(value, dict) and not isinstance(value, self.__class__):
            value = self.__class__(value)
        super(MagicDict, self).__setattr__(name, value)
        super(MagicDict, self).__setitem__(name, value)

    __setitem__ = __setattr__

    def update(self, e=None, **things):
        d = e or dict()
        d.update(things)
        for k in d:
            setattr(self, k, d[k])

    def pop(self, k, d=None):
        delattr(self, k)
        return super(MagicDict, self).pop(k, d)
