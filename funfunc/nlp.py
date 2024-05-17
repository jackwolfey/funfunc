# -*- coding: utf-8 -*-
# AUTHOR  : wjia
# TIME    : 2022/6/21 17:28
# FILE    : nlp
# PROJECT : funfunc
# IDE     : PyCharm
__all__ = ['Validator', 'replace_chinese', 'make_valid_filename']

import re


class Validator:

    @classmethod
    def is_url(cls, url_string: str) -> bool:
        pat = re.compile(r"^(http|https)://[0-9a-zA-Z.]*")
        if pat.match(url_string):
            return True
        else:
            return False

    @classmethod
    def is_chinese(cls, text: str) -> bool:
        pat = re.compile(u'[\u4E00-\u9FA5]')
        if re.match(pat, text):
            return True
        else:
            return False


def replace_chinese(text, replace_str: str = ' ') -> str:
    """
    replace all the chinese characters in text by replace_str
    """
    filtrate = re.compile(u'[\u4E00-\u9FA5]')
    text_without_chinese = filtrate.sub(rf'{replace_str}', text)
    return text_without_chinese


def make_valid_filename(filename, replaced_char='_') -> str:
    """
    make an invalid filename become valid
    """
    invalid_filename_chars = r'[<>:"/\\|?*\x00-\x1F]'
    return re.sub(invalid_filename_chars, replaced_char, filename)
