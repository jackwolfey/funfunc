# -*- coding: utf-8 -*-
# AUTHOR  : wjia
# TIME    : 2022/6/21 17:08
# FILE    : tool
# PROJECT : funfunc
# IDE     : PyCharm
import copy
import datetime
import functools
import json
import logging
import os
import time
import typing
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
    def wrapper(*args, **kwargs):
        start = time.time()
        result = method(*args, **kwargs)
        end = time.time()
        print('{} USED TIME:{}'.format(method.__name__, end - start))

        return result

    return wrapper


def time_it_precise(method):
    """similar to time_it but use more precise time.perf_counter()"""

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = method(*args, **kwargs)
        end = time.perf_counter()
        print('{} USED TIME:{}'.format(method.__name__, end - start))

        return result

    return wrapper


def quick_sort(arr: list) -> list:
    """classic sort algorithm"""
    if len(arr) < 2:
        return arr
    temp = arr[0]
    small = [i for i in arr[1:] if i <= temp]
    big = [i for i in arr[1:] if i > temp]
    return quick_sort(small) + [temp] + quick_sort(big)


def get_basic_logger(level=logging.INFO, fmt: str = None, datefmt: str = None, **kwargs):
    """fast way to create a logging.Logger object"""
    if fmt:
        log_format = fmt
    else:
        log_format = "%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s"

    if datefmt:
        log_datefmt = datefmt
    else:
        log_datefmt = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt=log_datefmt,
        **kwargs)

    logger = logging.getLogger(__name__)
    return logger


def chunks(arr: list, n: int) -> list:
    """split list to some lists with n items in it"""
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
        @functools.wraps(deprecated_func)
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

    def __init__(__self, *args, **kwargs):  # noqa
        object.__setattr__(__self, '__parent', kwargs.pop('__parent', None))
        object.__setattr__(__self, '__key', kwargs.pop('__key', None))
        object.__setattr__(__self, '__frozen', False)
        for arg in args:
            if not arg:
                continue
            elif isinstance(arg, dict):
                for key, val in arg.items():
                    __self[key] = __self._hook(val)
            elif isinstance(arg, tuple) and (not isinstance(arg[0], tuple)):
                __self[arg[0]] = __self._hook(arg[1])
            else:
                for key, val in iter(arg):
                    __self[key] = __self._hook(val)

        for key, val in kwargs.items():
            __self[key] = __self._hook(val)

    def __setattr__(self, name, value):
        if hasattr(self.__class__, name):
            raise AttributeError("'Dict' object attribute "
                                 "'{0}' is read-only".format(name))
        else:
            self[name] = value

    def __setitem__(self, name, value):
        isFrozen = (hasattr(self, '__frozen') and
                    object.__getattribute__(self, '__frozen'))
        if isFrozen and name not in super(MagicDict, self).keys():
            raise KeyError(name)
        super(MagicDict, self).__setitem__(name, value)
        try:
            p = object.__getattribute__(self, '__parent')
            key = object.__getattribute__(self, '__key')
        except AttributeError:
            p = None
            key = None
        if p is not None:
            p[key] = self
            object.__delattr__(self, '__parent')
            object.__delattr__(self, '__key')

    def __add__(self, other):
        if not self.keys():
            return other
        else:
            self_type = type(self).__name__
            other_type = type(other).__name__
            msg = "unsupported operand type(s) for +: '{}' and '{}'"
            raise TypeError(msg.format(self_type, other_type))

    @classmethod
    def _hook(cls, item):
        if isinstance(item, dict):
            return cls(item)
        elif isinstance(item, (list, tuple)):
            return type(item)(cls._hook(elem) for elem in item)
        return item

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __missing__(self, name):
        if object.__getattribute__(self, '__frozen'):
            raise KeyError(name)
        return self.__class__(__parent=self, __key=name)

    def __delattr__(self, name):
        del self[name]

    def to_dict(self):
        base = {}
        for key, value in self.items():
            if isinstance(value, type(self)):
                base[key] = value.to_dict()
            elif isinstance(value, (list, tuple)):
                base[key] = type(value)(
                    item.to_dict() if isinstance(item, type(self)) else
                    item for item in value)
            else:
                base[key] = value
        return base

    def copy(self):
        return copy.copy(self)

    def deepcopy(self):
        return copy.deepcopy(self)

    def __deepcopy__(self, memo):
        other = self.__class__()
        memo[id(self)] = other
        for key, value in self.items():
            other[copy.deepcopy(key, memo)] = copy.deepcopy(value, memo)
        return other

    def update(self, *args, **kwargs):
        other = {}
        if args:
            if len(args) > 1:
                raise TypeError()
            other.update(args[0])
        other.update(kwargs)
        for k, v in other.items():
            if ((k not in self) or
                    (not isinstance(self[k], dict)) or
                    (not isinstance(v, dict))):
                self[k] = v
            else:
                self[k].update(v)

    def __getnewargs__(self):
        return tuple(self.items())

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        self.update(state)

    def __or__(self, other):
        if not isinstance(other, (MagicDict, dict)):
            return NotImplemented
        new = MagicDict(self)
        new.update(other)
        return new

    def __ror__(self, other):
        if not isinstance(other, (MagicDict, dict)):
            return NotImplemented
        new = MagicDict(other)
        new.update(self)
        return new

    def __ior__(self, other):
        self.update(other)
        return self

    def setdefault(self, key, default=None):
        if key in self:
            return self[key]
        else:
            self[key] = default
            return default

    def freeze(self, shouldFreeze=True):
        object.__setattr__(self, '__frozen', shouldFreeze)
        for key, val in self.items():
            if isinstance(val, MagicDict):
                val.freeze(shouldFreeze)

    def unfreeze(self):
        self.freeze(False)


class OptClass:
    """
    let you create a Option class by a list of option names of predefined options dict
    .json class property can convert options to json format string

    Example:
        # init by list of option names
        opt_names = ['use_gpu', 'workers', 'batch_size']
        opts = OptClass(opt_names)
        opts.use_gpu = True
        opts.workers = 2

        # init by predefined options dict
        opts_dict = {'use_gpu': True, 'workers': 2, 'batch_size': 16}
        opts = OptClass(opts_dict)
        print(opts.use_gpu)
        print(opts.json)
    """

    def __init__(self, option_names):
        if isinstance(option_names, list):
            for opt in option_names:
                if not isinstance(opt, str):
                    opt_str = str(opt)
                    setattr(self, opt_str, None)
                else:
                    setattr(self, opt, None)
        elif isinstance(option_names, dict):
            for k, v in option_names.items():
                if not isinstance(k, str):
                    opt_str = str(k)
                    setattr(self, opt_str, v)
                else:
                    setattr(self, k, v)
        else:
            raise TypeError(f'Unsupported option_names type: {type(option_names)}, please pass a list or dict object')

    @property
    def json(self):
        return json.dumps(self.__dict__)


def get_all_abspath_from_folder(folder_path: str, get_relative: bool = False, file_only: bool = True) -> list:
    """
    get all files path of a path or a folder, if file_only=False, include folder

    :param folder_path: target folder_path, a path-like string
    :param get_relative: if True, will return relative path instead of abspath
    :param file_only: if False, will return folder's path in folder_path
    """
    if not get_relative:
        folder_path = os.path.abspath(folder_path)

    if not file_only:
        return [os.path.join(folder_path, i) for i in os.listdir(folder_path)]

    return [os.path.join(folder_path, i) for i in os.listdir(folder_path) if
            os.path.isfile(os.path.join(folder_path, i))]


def is_in_docker():
    return os.path.exists('/workspace')


def get_methods(instance):
    methods = [m for m in dir(instance) if callable(getattr(instance, m)) and not m.startswith("__")]
    return methods


def get_args_info(name, opt):
    return f'{name}: ' + ', '.join(f'{k}={v}' for k, v in vars(opt).items())


def try_except_print(func):
    """
    auto add try except to a function, use @try_except_print decorator
    """

    @functools.wraps(func)
    def handler(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f'Exception From {func.__name__}: {e}')

    return handler


def retry(retry_count: int = 5, sleep_time: int = 1):
    """
    retry to call a function when it raise an error
    """

    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            for i in range(retry_count):
                try:
                    res = func(*args, **kwargs)
                    return res
                except:
                    time.sleep(sleep_time)
                    continue
            return None

        return inner

    return wrapper


Flexible = typing.Any  # use this to mark something could be modified
