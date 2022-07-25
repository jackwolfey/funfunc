# -*- coding: utf-8 -*-
# AUTHOR  : wjia
# TIME    : 2022/6/21 16:02
# FILE    : __init__
# PROJECT : funfunc
# IDE     : PyCharm
__VERSION__ = "0.1.8"
__AUTHOR__ = "Wei Jia"
__DESCRIPTION__ = "Make Py Development Much Easier & Fun"
__all__ = [
    'base64_string_to_pil_image',
    'pil_image_to_base64_string',
    'image_array_to_pil_image',
    'pil_image_to_image_array',
    'base64_string_to_image_array',
    'image_array_to_base64_string',
    'get_device_torch',
    'pandas_max_print',
    'Validator',
    'get_current_str_time',
    'download_file',
    'time_it',
    'quick_sort',
    'get_basic_logger',
    'chunks',
    'get_host_ip',
    'time_to_timestamp',
    'second_to_strtime',
    'set_deprecated',
    'indented_json_string',
    'train_test_split_arr',
    'MagicDict',
    'OptClass',
    'rotate_image',
    'get_all_abspath_from_folder',
    'replace_chinese'
]

from .cv import *
from .dl import *
from .ml import *
from .nlp import *
from .tool import *
